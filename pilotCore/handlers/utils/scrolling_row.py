import re

from telegram import InlineKeyboardButton




# PAGE SCROLL:
def scroll_layout_handler(current_page: int, pages_num: int) -> list:
    """Lauout for scroling row"""
    current_page_marker = u'\U000025CF'
    page_selected = current_page
    pages_num = pages_num + 1

    print('page_selected ' + str(page_selected))
    print('pages_num ' + str(pages_num))

    max_listing_num = 5 if pages_num >= 5 else pages_num

    if pages_num > 5:
        if page_selected <= 3:
            pages_layout = list(range(0, 5))
            ind = pages_layout.index(page_selected)
            pages_layout[ind] = current_page_marker
        elif page_selected >= pages_num - 3:
            pages_layout = list(range(pages_num - 5, pages_num))
            ind = pages_layout.index(page_selected)
            pages_layout[ind] = current_page_marker
        else:
            pages_layout = list(range(page_selected - 2, page_selected + 3))
            ind = pages_layout.index(page_selected)
            pages_layout[ind] = current_page_marker
    else:
        pages_layout = list(range(0, pages_num))
        pages_layout[page_selected] = current_page_marker
    return pages_layout


def scroll_layout_keyboard(layout: list, num_callback: str, left_callback: str, right_callback: str) -> list:
    """Keyboard layout for scrolling row"""
    scroll_row = []
    # left arrow:
    left_button = [
        InlineKeyboardButton(
            str('<'),
            callback_data=left_callback
        ),
    ]
    scroll_row.extend(left_button)
    # numbers scroller (5 pages by dafault):
    number_buttons_layout = []
    for value in layout:
        if value != '\U000025CF':
            value_view = int(value) + 1
        else:
            value_view = value
        number_buttons_layout.append(
            InlineKeyboardButton(
                str(value_view),
                callback_data=f'{num_callback}:{value}'
                # callback_data=f'cb:{value}'
            ),
        )
    scroll_row.extend(number_buttons_layout)
    # right_arrow:
    right_button = [
        InlineKeyboardButton(
            str('>'),
            callback_data=right_callback
        )
    ]
    scroll_row.extend(right_button)
    return scroll_row


### !!! ###
def scroll_layout_model_page(modObj: object, pageAttr: str, pages: int, value: int) -> int:
    """Keyboard layout model for current page"""
    if value == 0:
        setattr(modObj, pageAttr, 0)
    if value == -1:
        setattr(
            modObj,
            pageAttr,
            (
                pages if getattr(modObj, pageAttr) == 0
                else getattr(modObj, pageAttr) - 1
            )
        )
    if value == -2:
        setattr(
            modObj,
            pageAttr,
            (
                0 if getattr(modObj, pageAttr) == pages
                else getattr(modObj, pageAttr) + 1
            )
        )
    if re.match('^[+]?\d+', str(value)):
        setattr(modObj, pageAttr, value)
    modObj.save()
    return getattr(modObj, pageAttr)

# def scroll_layout_model_pages(modObj: object, pageAttr: str, pagesAttr: str, value: int) -> int:
#     """Keyboard layout model for pages number"""
#     if getattr(modObj, pagesAttr) != value:
#         setattr(modObj, pageAttr, 0)
#         setattr(modObj, pagesAttr, value)
#     modObj.save()
#     return getattr(modObj, pagesAttr)

# def scroll_layout_model_page(modObj: object, pageAttr: str, pagesAttr: str, value: int) -> int:
#     """Keyboard layout model for current page"""
#     if value == 0:
#         setattr(modObj, pageAttr, 0)
#     if value == -1:
#         setattr(
#             modObj,
#             pageAttr,
#             (
#                 getattr(modObj, pagesAttr) if getattr(modObj, pageAttr) == 0
#                 else getattr(modObj, pageAttr) - 1
#             )
#         )
#     if value == -2:
#         setattr(
#             modObj,
#             pageAttr,
#             (
#                 0 if getattr(modObj, pageAttr) == getattr(modObj, pagesAttr)
#                 else getattr(modObj, pageAttr) + 1
#             )
#         )
#     if re.match('^[+]?\d+', str(value)):
#         setattr(modObj, pageAttr, value)
#     modObj.save()
#     return getattr(modObj, pageAttr)
#
# def scroll_layout_model_pages(modObj: object, pageAttr: str, pagesAttr: str, value: int) -> int:
#     """Keyboard layout model for pages number"""
#     if getattr(modObj, pagesAttr) != value:
#         setattr(modObj, pageAttr, 0)
#         setattr(modObj, pagesAttr, value)
#     modObj.save()
#     return getattr(modObj, pagesAttr)
