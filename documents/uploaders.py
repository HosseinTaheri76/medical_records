def test_document_uploader(instance, filename):
    return f'{instance.patient.name}/tests/{filename}'


def other_doc_uploader(instance, filename):
    return f'{instance.patient.name}/{instance.doc_type}/{filename}'


def prescription_img_uploader(instance, filename):
    return f'{instance.patient.name}/visits/{instance.visit_date}/{filename}'
