# Script: `.\scripts\interface.py`

# Imports
import gradio as gr
import time, threading
from scripts.database import add_event, get_events_in_window
from scripts.utility import get_61_day_window, generate_recurrences  # Assume these are implemented
from scripts.temporary import events_state

# Functions
def launch_interface(config, save_config, port=7860):
    import threading
    import time
    from datetime import datetime
    from scripts.database import get_events_in_window
    from scripts.utility import get_61_day_window, generate_recurrences, validate_config

    interrupt_event = threading.Event()
    skip_event = threading.Event()

    def load_events():
        """Load events from database and generate recurrences"""
        start, end = get_61_day_window()
        db_events = get_events_in_window(start, end)
        all_events = []
        for event in db_events:
            all_events.extend(generate_recurrences(event, start, end))
        return sorted(all_events, key=lambda x: x["start_time"])

    def save_and_start(event_titles, start_times, end_times, recurrences, notes):
        """Handle event submission and validation"""
        from scripts.database import add_event, delete_all_events
        
        error_messages = []
        new_events = []

        # Split inputs
        titles = [t.strip() for t in event_titles.strip().split("\n") if t.strip()]
        starts = [s.strip() for s in start_times.strip().split("\n")]
        ends = [e.strip() for e in end_times.strip().split("\n")]
        recs = [r.strip().lower() for r in recurrences.strip().split("\n")]
        notes_list = [n.strip() for n in notes.strip().split("\n")]

        # Validate line counts
        line_counts = {len(titles), len(starts), len(ends), len(recs), len(notes_list)}
        if len(line_counts) > 1:
            return (
                "Error: All fields must have equal lines",
                gr.update(visible=True),
                gr.update(visible=False),
                []
            )

        # Validate individual entries
        for i in range(len(titles)):
            title = titles[i]
            start = starts[i]
            end = ends[i]
            rec = recs[i]
            note = notes_list[i]

            try:
                if not title:
                    raise ValueError(f"Row {i+1}: Title required")

                start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
                end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")
                
                if start_dt >= end_dt:
                    raise ValueError(f"Row {i+1}: End time must be after start")

                if rec not in {"daily", "weekly", "monthly", "none"}:
                    rec = "none"

                new_events.append((title, start, end, rec, note))

            except ValueError as e:
                error_messages.append(f"Row {i+1}: {str(e)}")
            except Exception as e:
                error_messages.append(f"Row {i+1}: Invalid data - {str(e)}")

        # Only commit if validation passed
        if not error_messages:
            delete_all_events()
            for title, start, end, rec, note in new_events:
                add_event(
                    title=title,
                    start_time=start,
                    end_time=end,
                    recurrence_rule=rec,
                    notes=note,
                    is_recurring=int(rec != "none")
                )
            
            db_events = load_events()
            valid_events = validate_config(db_events)
            
            return (
                "Schedule saved!" if valid_events else "No valid events!",
                gr.update(visible=False),
                gr.update(visible=True),
                valid_events
            )
        
        return (
            "\n".join(error_messages),
            gr.update(visible=True),
            gr.update(visible=False),
            []
        )

    def run_schedule(events):
        """Threaded schedule executor with progress updates"""
        def _run_thread():
            for event in events:
                if interrupt_event.is_set():
                    break

                start = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M")
                end = datetime.strptime(event["end_time"], "%Y-%m-%d %H:%M")
                duration = (end - start).total_seconds()

                # Wait for event start time
                while datetime.now() < start and not interrupt_event.is_set():
                    time.sleep(1)

                # Update UI elements through queue
                app.queue().put(
                    (current_event.update, {"value": f"Active: {event['title']}"})
                )

                start_time = time.time()
                while (time.time() - start_time) < duration and not interrupt_event.is_set():
                    elapsed = time.time() - start_time
                    progress = (elapsed / duration) * 100
                    app.queue().put([
                        (progress_bar.update, {"value": progress}),
                        (current_event.update, {"value": f"{event['title']} - {int(duration - elapsed)}s left"})
                    ])
                    time.sleep(1)

                if not interrupt_event.is_set():
                    app.queue().put(
                        (current_event.update, {"value": f"Completed: {event['title']}"}))

        threading.Thread(target=_run_thread, daemon=True).start()

    def stop_execution():
        """Handle execution stopping"""
        interrupt_event.set()
        return gr.update(visible=False), gr.update(visible=True)

    def load_initial_events():
        """Load existing events into input fields"""
        events = load_events()
        titles = [e["title"] for e in events]
        starts = [e["start_time"] for e in events]
        ends = [e["end_time"] for e in events]
        recs = [e["recurrence_rule"] for e in events]
        notes = [e["notes"] for e in events]
        return (
            "\n".join(titles),
            "\n".join(starts),
            "\n".join(ends),
            "\n".join(recs),
            "\n".join(notes)
        )

    # In Gradio setup:
    app.load(
        load_initial_events,
        inputs=None,
        outputs=[event_titles, start_times, end_times, recurrences, notes]
    )

    # Build Gradio interface
    with gr.Blocks() as app:
        # Configuration Section
        with gr.Row(visible=True) as configure_page:
            event_titles = gr.Textbox(lines=10, label="Event Titles",
                                    placeholder="Enter one event per line")
            start_times = gr.Textbox(lines=10, label="Start Times (YYYY-MM-DD HH:MM)",
                                   placeholder="2023-10-25 09:00\n2023-10-25 13:00")
            end_times = gr.Textbox(lines=10, label="End Times (YYYY-MM-DD HH:MM)",
                                 placeholder="2023-10-25 12:00\n2023-10-25 14:00")
            recurrences = gr.Textbox(lines=10, label="Recurrence Rules",
                                   placeholder="none\ndaily\nweekly")
            notes = gr.Textbox(lines=10, label="Notes",
                              placeholder="Add notes or descriptions here")
            status = gr.Textbox(label="Status", interactive=False)
            save_btn = gr.Button("Save & Start Schedule", variant="primary")

        # Execution Section
        with gr.Row(visible=False) as execution_page:
            current_event = gr.Textbox(label="Current Event", interactive=False)
            progress_bar = gr.Slider(0, 100, label="Progress", interactive=False)
            stop_btn = gr.Button("Stop Execution", variant="stop")

        # Event Handlers
        save_btn.click(
            save_and_start,
            inputs=[event_titles, start_times, end_times, recurrences, notes],
            outputs=[status, configure_page, execution_page, events_state]
        )
        stop_btn.click(
            stop_execution,
            inputs=None,
            outputs=[execution_page, configure_page]
        )

        # Initialization
        app.load(
            load_initial_events,
            inputs=None,
            outputs=events_state
        )

        app.launch(server_name="0.0.0.0", server_port=port)