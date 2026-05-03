import flet as ft
def main(page: ft.Page):
    def open_bs(e):
        col = ft.Column([ft.Text(f"Item {i}") for i in range(50)], scroll=ft.ScrollMode.AUTO)
        bs = ft.BottomSheet(
            content=ft.Container(
                content=col,
                bgcolor="blue",
                padding=20,
            )
        )
        page.overlay.append(bs)
        bs.open = True
        page.update()
    page.add(ft.ElevatedButton("Open", on_click=open_bs))
ft.app(target=main)
