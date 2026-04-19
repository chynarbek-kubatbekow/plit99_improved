import logging

from django.db import OperationalError, ProgrammingError
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger(__name__)
ADMIN_DB_EXCEPTIONS = (OperationalError, ProgrammingError)


class AdminDatabaseGuardMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if not request.path.startswith('/admin'):
            return None

        if not isinstance(exception, ADMIN_DB_EXCEPTIONS):
            return None

        logger.exception(
            'Admin request failed because the database is unavailable: %s',
            request.path,
        )
        return render(
            request,
            'core/admin_unavailable.html',
            status=503,
        )
