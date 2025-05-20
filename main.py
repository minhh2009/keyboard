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

    key_rows = [
        list("QWERTYUIOP"),
        list("ASDFGHJKL"),
        list("ZXCVBNM")
    ]

    def textbtns(text, data, width=50, height=50):
        return ft.GestureDetector(
            content=ft.TextButton(content=ft.Text(text, size=20), on_click=press, data=data, width=width, height=height),
            on_long_press_start=start_repeat,
            on_long_press_end=stop_repeat,
            data=data
        )

    for row in key_rows:
        btns = []
        for k in row:
            btns.append(
                textbtns(k, k.lower())
            )
        page.add(ft.Row(btns, spacing=5, alignment="center"))

    space_btn = textbtns("Space", " ", width=200, height=50)

    page.add(ft.Row([space_btn], spacing=5, alignment="center"))


if __name__ == "__main__":
    ft.app(target=main)
