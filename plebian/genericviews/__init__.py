from plebian.genericviews.base import View, TemplateView, RedirectView
from plebian.genericviews.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView,
                                     WeekArchiveView, DayArchiveView, TodayArchiveView,
                                     DateDetailView)
from plebian.genericviews.detail import DetailView
from plebian.genericviews.edit import CreateView, UpdateView, DeleteView
from plebian.genericviews.list import ListView


class GenericViewError(Exception):
    """A problem in a generic view."""
    pass
