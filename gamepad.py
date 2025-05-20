import flet as ft
import asyncio
import pydirectinput

async def main(page: ft.Page):
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    presses = {}

    def press(e: ft.ControlEvent):
        pydirectinput.keyDown(e.control.data)                         
        pydirectinput.keyUp(e.control.data)

    async def repeat(e):
        while presses[e.control.data]:
            pydirectinput.keyDown(e.control.data)
            await asyncio.sleep(0.01)                                                                                                                                                                                                                                                                                                                                                  

    async def start_repeat(e):
        presses.setdefault(e.control.data, True)
        asyncio.create_task(repeat(e))

    async def stop_repeat(e):
        presses[e.control.data] = False                                            
        pydirectinput.keyUp(e.control.data)

    def iconbtns(icon, data):
        return ft.GestureDetector(
            content=ft.IconButton(icon, on_click=press, data=data, icon_size=64),
            on_long_press_start=start_repeat,
            on_long_press_end=stop_repeat,
            data=data
        )
    
    def textbtns(text, data):
        return ft.GestureDetector(
            content=ft.TextButton(content=ft.Text(text, size=32), on_click=press, data=data, width=64, height=64),
            on_long_press_start=start_repeat,
            on_long_press_end=stop_repeat,
            data=data
        )

    pad1 = ft.Column(
        [
            iconbtns(ft.Icons.KEYBOARD_ARROW_UP, "up"),
            ft.Row([
                iconbtns(ft.Icons.KEYBOARD_ARROW_LEFT, "left"),
                ft.Text(width=84),
                iconbtns(ft.Icons.KEYBOARD_ARROW_RIGHT, "right"),
            ], alignment="center"),
            iconbtns(ft.Icons.KEYBOARD_ARROW_DOWN, "down"),
        ],
        spacing=10,
        horizontal_alignment="center",
    )

    pad2 = ft.Column(
        [
            textbtns("Y", "y"),
            ft.Row([
                textbtns("X", "x"),
                ft.Text(width=84),
                textbtns("B", "b"),
            ], alignment="center"),
            textbtns("A", "a"),
        ],
        spacing=10,
        horizontal_alignment="center",
    )

    page.add(
        ft.Row(
            [
                pad1,
                pad2,
            ], 
            spacing=50, 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
    )

if __name__ == "__main__":
    ft.app(target=main)
