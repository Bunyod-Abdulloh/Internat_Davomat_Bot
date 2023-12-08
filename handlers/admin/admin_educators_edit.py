from aiogram import types

from loader import dp
from states.admin_state import AdminEditEdicators


# a_e_e = Admin educator edit (handlers/admin/file-name)
@dp.callback_query_handler(state=AdminEditEdicators.main)
async def a_e_e_edit(call: types.CallbackQuery):
    print(call.data)
    educator_id = call.data.split("_")[-1]

    if call.data.__contains__("aeebname_"):
        await AdminEditEdicators.edit_fullname.set()

    # elif call.data.__contains__("")
    print(educator_id)
