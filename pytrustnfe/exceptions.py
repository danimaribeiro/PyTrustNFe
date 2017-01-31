# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


class NFeValidationException(ValueError):
    """Exceção para erro na validação do esquema da NFe"""

    def __init__(self, message, *args, **kwargs):
        self.erros = kwargs['erros']
        self.sent_xml = kwargs['sent_xml']
        super(NFeValidationException, self).__init__(message, *args, **kwargs)
