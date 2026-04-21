import flet as ft
from db import main_db 


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Список покупок"

    purchase_list = ft.Column()

    filter_type = 'all'

    def load_tasks():
        purchase_list.controls.clear()
        for purchase_id, purchase_text, bought in main_db.get_purchase(filter_type=filter_type):
            purchase_list.controls.append(view_purchase(
                purchase_id=purchase_id,
                purchase_text=purchase_text,
                bought=bought
                ))


    def view_purchase(purchase_id, purchase_text, bought=None):
        checkbox = ft.Checkbox(
            value=bool(bought),
            on_change=lambda e: toggle_purchase(purchase_id=purchase_id, is_bought=e.control.value)
            )

        purchase_field = ft.TextField(read_only=True, value=purchase_text, expand=True)

        def delete(e):
            main_db.delete_purchase(purchase_id)
            load_tasks()

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

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_purchase)


        return ft.Row([checkbox, purchase_field, edit_button, save_button, delete_button])
    
    def toggle_purchase(purchase_id, is_bought):
        print(is_bought)
        main_db.update_purchase(purchase_id=purchase_id, bought=int(is_bought))
        load_tasks()

    def add_purchase(e):
        if purchase_input.value:
            purchase = purchase_input.value
            purchase_id = main_db.add_purchase(purchase=purchase)
            print(f'Покупка {purchase} добавлена! Его ID - {purchase_id}')
            purchase_list.controls.append(view_purchase(purchase_id=purchase_id, purchase_text=purchase))
            purchase_input.value = None


    purchase_input = ft.TextField(label="Введите покупку", expand=True, on_submit=add_purchase)

    purchase_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_purchase)

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()
        

    filter_buttons = ft.Row([
        ft.ElevatedButton('Все покупки', on_click=lambda e: set_filter('all'), icon=ft.Icons.ALL_INBOX, icon_color=ft.Colors.BLACK),
        ft.ElevatedButton('Купленные', on_click=lambda e: set_filter('bought'), icon=ft.Icons.CHECK_BOX, icon_color=ft.Colors.GREEN_900),
        ft.ElevatedButton('Некупленные', on_click=lambda e: set_filter('unbought'), icon=ft.Icons.CHECK_BOX_OUTLINE_BLANK, icon_color=ft.Colors.GREEN_900),
        ft.ElevatedButton('Удалить Купленные', icon=ft.Icons.DELETE, on_click=lambda e: (main_db.delete_bought_purchases() , load_tasks()), icon_color=ft.Colors.RED_900)

    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)


    send_task = ft.Row([purchase_input, purchase_button])

    page.add(send_task, filter_buttons, purchase_list)
    load_tasks()


if __name__ == "__main__":
    main_db.init_db()
    ft.run(main, view=ft.AppView.WEB_BROWSER)