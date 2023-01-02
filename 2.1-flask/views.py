from flask import request, jsonify
from flask.views import MethodView
import pydantic

from models import Session, Advt
from schema import CreateAdvtSchema, PatchAdvtSchema
from errors import HttpError


def get_advt(advt_id: int, session: Session) -> Advt:
    advt = session.query(Advt).get(advt_id)
    if advt is None:
        raise HttpError(404, 'Advertisement not found')
    return advt


class AdvtViews(MethodView):

    def get(self, advt_id: int):
        with Session() as session:
            advt = get_advt(advt_id, session)

            return jsonify({
                            'id': advt.id,
                            'author': advt.author,
                            'title': advt.title,
                            'description': advt.description,
                            'creation_time': advt.creation_time
                            })

    def post(self):
        json_data = dict(request.json)
        try:
            json_data_validate = CreateAdvtSchema(**json_data).dict()
        except pydantic.ValidationError as err:
            raise HttpError(400, err.errors())

        with Session() as session:
            new_advt = Advt(**json_data_validate)
            session.add(new_advt)
            session.commit()

            return jsonify({'status': 'success',
                            'id': new_advt.id,
                            'author': new_advt.author,
                            'title': new_advt.title,
                            'description': new_advt.description,
                            'creation_time': new_advt.creation_time
                            })

    def patch(self, advt_id: int):
        json_data = dict(request.json)
        try:
            json_data_validate = PatchAdvtSchema(**json_data).dict()
        except pydantic.ValidationError as err:
            raise HttpError(400, err.errors())

        with Session() as session:
            advt = get_advt(advt_id, session)
            for key, value in json_data_validate.items():
                setattr(advt, key, value)
            session.add(advt)
            session.commit()

        return jsonify({'status': 'success',
                        'id': advt.id,
                        'author': advt.author,
                        'title': advt.title,
                        'description': advt.description,
                        'creation_time': advt.creation_time
                        })

    def delete(self, advt_id: int):
        with Session() as session:
            advt = get_advt(advt_id, session)
            session.delete(advt)
            session.commit()

        return jsonify({'status': 'delete',
                        'id': advt.id,
                        'author': advt.author,
                        'title': advt.title
                        })
