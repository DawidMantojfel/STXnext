from datetime import datetime


def convert_date(published_date):
    """
    converts date from str to datetime object
    :param published_date:
    :return: datetime object
    """
    # if there is no date
    if published_date is None:
        return None
    date = published_date.split('-')
    # if published date has only year
    if len(date) == 1:
        data_result = datetime.strptime(published_date, '%Y')
    # if published date has year and month
    elif len(date) == 2:
        data_result = datetime.strptime(' '.join(date), "%Y %m")
    # if published date is in day-moth-year format
    else:
        data_result = datetime.strptime(' '.join(date), "%Y %m %d")
    return data_result


def convert_initials(name):
    """
    converts full name into initials
    :param name:
    :return: initials of name
    """
    full_name = name.split()
    new_name = ''
    for i in range(len(full_name)-1):
        initial = full_name[i]
        new_name += initial[0].upper() + '. '
    new_name += full_name[-1].title()
    return new_name

