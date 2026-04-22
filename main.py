import flet as ft
from db import main_db 


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Список покупок"

    purchase_list = ft.Column()
    count = ft.Text()

    filter_type = 'all'


    def load_purchases():
        purchase_list.controls.clear()

        purchases = main_db.get_purchase(filter_type=filter_type)

        bought_count = 0

        for purchase_id, purchase_text, bought, quantity in purchases:

            if bought:
                bought_count += 1

            purchase_list.controls.append(view_purchase(
                purchase_id=purchase_id,
                purchase_text=purchase_text,
                bought=bought,
                quantity=quantity
            ))

        count.value = f'Всего: {len(purchases)} | Куплено: {bought_count}'
        page.update()


    def view_purchase(purchase_id, purchase_text, bought=None, quantity=1):
        checkbox = ft.Checkbox(
            value=bool(bought),
            on_change=lambda e: toggle_purchase(purchase_id=purchase_id, is_bought=e.control.value)
        )

        purchase_field = ft.TextField(read_only=True, value=purchase_text, expand=True)

        quantity_text = ft.Text(f"x{quantity}")

        def delete(e):
            main_db.delete_purchase(purchase_id)
            load_purchases()

        delete_button = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=delete)

        def enable_edit(e):
            if purchase_field.read_only == True:
                purchase_field.read_only = False
            else:
                purchase_field.read_only = True

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_purchase(e):
            main_db.update_purchase(purchase_id=purchase_id, new_purchase=purchase_field.value)
            purchase_field.read_only = True
            load_purchases()

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_purchase)

        return ft.Row([checkbox, purchase_field, quantity_text, edit_button, save_button, delete_button])
    

    def toggle_purchase(purchase_id, is_bought):
        main_db.update_purchase(purchase_id=purchase_id, bought=int(is_bought))
        load_purchases()


    def add_purchase(e):
        if purchase_input.value:
            purchase = purchase_input.value

            quantity = int(quantity_input.value) if quantity_input.value else 1

            purchase_id = main_db.add_purchase(purchase=purchase, quantity=quantity)

            purchase_input.value = ""
            quantity_input.value = ""

            load_purchases()


    purchase_input = ft.TextField(label="Введите покупку", expand=True, on_submit=add_purchase)

    quantity_input = ft.TextField(label="Кол-во", width=100, on_submit=add_purchase)

    purchase_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_purchase)


    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_purchases()
        

    filter_buttons = ft.Row([
    ft.ElevatedButton('Все покупки', on_click=lambda e: set_filter('all'), icon=ft.Icons.ALL_INBOX, icon_color=ft.Colors.BLACK),
    ft.ElevatedButton('Купленные', on_click=lambda e: set_filter('bought'), icon=ft.Icons.CHECK_BOX, icon_color=ft.Colors.GREEN_900),
    ft.ElevatedButton('Некупленные', on_click=lambda e: set_filter('unbought'), icon=ft.Icons.CHECK_BOX_OUTLINE_BLANK, icon_color=ft.Colors.GREEN_900),
    ft.ElevatedButton('Удалить Купленные', icon=ft.Icons.DELETE, on_click=lambda e: (main_db.delete_bought_purchases(), load_purchases()), icon_color=ft.Colors.RED_900)
], alignment=ft.MainAxisAlignment.SPACE_AROUND)

     
    send_purchase = ft.Row([purchase_input, quantity_input, purchase_button])

    page.add(send_purchase, filter_buttons, purchase_list, count)

    load_purchases()


if __name__ == "__main__":
    main_db.init_db()
    ft.run(main, view=ft.AppView.WEB_BROWSER)