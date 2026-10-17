from nicegui import ui


def open_file(on_file, accept="*"):
    with ui.dialog() as dialog, ui.card():

        async def handle_upload(e):
            data = await e.file.read()
            dialog.close()
            on_file(e.file.name, data)

        ui.upload(on_upload=handle_upload, auto_upload=True).props(f'accept="{accept}"')

    dialog.open()