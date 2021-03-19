import json
import os

from flask import Flask, render_template, request, redirect, url_for, abort

from talk_to_back import BackendTalker

application = Flask(__name__)

talker = BackendTalker(port=7001, host="192.168.0.109")

TOKENS = ['123']

def check_token(token):
    if token in TOKENS:
        return True
    else:
        return False

@application.route('/')
def hello_world():
    return "HighLevelAPI made by ПиФла"

@application.route('/auth', methods=["POST"])
def auth():
    pass

@application.route("/reg", methods=["POST"])
def reg():
    pass

@application.route('/<token>/get_scheme')
def ret_scheme(token):
    if not check_token(token):
        abort(400, "no permission")
    return redirect(talker.adr + "/get_storage_scheme")


@application.route('/<token>/get_list_of_items_main_json')
def ret_all_storage(token):
    if not check_token(token):
        abort(400, "no permission")

    data = talker.get_list_of_all()
    _ = []
    for i in data:
        _.append({
            "name": i.name,
            "merged": 0 if i.merged else 1,
            "group_of_merge": str(i.group_of_merge),
            "merged_with": "" if not i.merged else str(i.merged_with),
            "size_width": i.size_width,
            "size_height": i.size_height,
            "size_depth": i.size_depth,
            "busy": 0 if i.busy else 1,
            "contained_item": "" if not i.busy else {
                "name": i.contained_item.name,
                "height": i.contained_item.original_height,
                "width": i.contained_item.original_width,
                "depth": i.contained_item.original_depth,
                "mass": i.contained_item.mass,
                "uuid": i.contained_item.uuid
            }
        })

    return json.dumps(_)


@application.route("/<token>/get_cell_json")
def get_cell(token):
    if not check_token(token):
        abort(400, "no permission")

    cell_name = request.args.getlist("cell_name")[0]
    i = talker.get_cell(cell_name)
    if i != "Неправильная ячейка":
        _ = {
            "name": i.name,
            "merged": 0 if i.merged else 1,
            "group_of_merge": str(i.group_of_merge),
            "merged_with": "" if not i.merged else str(i.merged_with),
            "size_width": i.size_width,
            "size_height": i.size_height,
            "size_depth": i.size_depth,
            "busy": 0 if i.busy else 1,
            "contained_item": "" if not i.busy else {
                "name": i.contained_item.name,
                "height": i.contained_item.original_height,
                "width": i.contained_item.original_width,
                "depth": i.contained_item.original_depth,
                "mass": i.contained_item.mass,
                "uuid": i.contained_item.uuid
            }}
    else:
        _ = "Неправильная ячейка"
    return json.dumps(_)


@application.route("/<token>/get_data_from_uuid_json")
def get_data_from_uuid_json(token):
    if not check_token(token):
        abort(400, "no permission")

    uuid = request.args.getlist("uuid")[0]

    i = talker.get_data_to_search_by_item(uuid)
    if i != "Неправильный uuid":
        _ = {
            "name": i.name,
            "merged": 0 if i.merged else 1,
            "group_of_merge": str(i.group_of_merge),
            "merged_with": "" if not i.merged else str(i.merged_with),
            "size_width": i.size_width,
            "size_height": i.size_height,
            "size_depth": i.size_depth,
            "busy": 0 if i.busy else 1,
            "contained_item": "" if not i.busy else {
                "name": i.contained_item.name,
                "height": i.contained_item.original_height,
                "width": i.contained_item.original_width,
                "depth": i.contained_item.original_depth,
                "mass": i.contained_item.mass,
                "uuid": i.contained_item.uuid
            }}
    else:
        _ = "Неправильный uuid"

    return json.dumps(_)


@application.route("/<token>/get_item_from_storage_json")
def get_item_from_storage_json(token):
    if not check_token(token):
        abort(400, "no permission")

    try:
        data_about_position = request.args.getlist("id")[0]
    except:
        return json.dumps("No argument found")
    _resp = talker.get(data_about_position)
    return _resp


@application.route("/<token>/get_remote_json")
def get_remote_json(token):
    if not check_token(token):
        abort(400, "no permission")

    _resp = talker.get_remote()
    if _resp == "Empty":
        return "Empty"
    _ = []
    for i in _resp:
        _.append({
            "name": i.name,
            "height": i.original_height,
            "width": i.original_width,
            "depth": i.original_depth,
            "mass": i.mass,
            "uuid": i.uuid
        })
    return json.dumps(_)


@application.route("/<token>/put/<filename>", methods=["POST"])
def handle_with_uploaded(token, filename):
    if not check_token(token):
        abort(400, "no permission")

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories allowed")

    directory = os.getcwdb().decode() + f"/static/uploads/{token}"

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f"{directory}/{filename}", "wb") as f:
        f.write(request.data)

    _resp = talker.put(request.data)

    #TODO: сохранение pdf отчетов на сервере

    return json.dumps(_resp)


@application.route("/<token>/pdf_main")
def pdf_main(token):
    if not check_token(token):
        abort(400, "no permission")

    return redirect(talker.adr + "/get_pdf_main")


@application.route("/<token>/pdf_remote")
def pdf_remote(token):
    if not check_token(token):
        abort(400, "no permission")

    return redirect(talker.adr + "/get_pdf_remote")


if __name__ == '__main__':
    application.run(host="192.168.0.109", port=7002)
