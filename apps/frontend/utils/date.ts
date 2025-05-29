import { format, formatDistance, isToday, isYesterday } from 'date-fns';

export const formatRelativeTime = (date: Date | string): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  const now = new Date();

  if (isNaN(dateObj.getTime())) {
    return '';
  }

  const diffInSeconds = Math.floor((now.getTime() - dateObj.getTime()) / 1000);
  if (diffInSeconds < 60) {
    return 'just now';
  }

  if (isToday(dateObj)) {
    return format(dateObj, 'h:mm a');
  }

  if (isYesterday(dateObj)) {
    return 'yesterday';
  }

  if (diffInSeconds < 7 * 24 * 60 * 60) {
    return formatDistance(dateObj, now, { addSuffix: true });
  }

  if (dateObj.getFullYear() === now.getFullYear()) {
    return format(dateObj, 'MMM d');
  }

  return format(dateObj, 'MMM d, yyyy');
};

export const formatTime = (date: Date | string): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;

  if (isNaN(dateObj.getTime())) {
    return '';
  }

  return format(dateObj, 'h:mm a');
};

export const formatChatTimestamp = (date: Date | string): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  const now = new Date();

  if (isNaN(dateObj.getTime())) {
    return '';
  }

  if (isToday(dateObj)) {
    return format(dateObj, 'h:mm a');
  }

  if (isYesterday(dateObj)) {
    return `Yesterday, ${format(dateObj, 'h:mm a')}`;
  }

  const diffInDays = Math.floor((now.getTime() - dateObj.getTime()) / (1000 * 60 * 60 * 24));
  if (diffInDays < 7) {
    return format(dateObj, 'EEEE, h:mm a');
  }

  if (dateObj.getFullYear() === now.getFullYear()) {
    return format(dateObj, 'MMM d, h:mm a');
  }

  return format(dateObj, 'MMM d, yyyy, h:mm a');
};

export const formatDate = (
  date: Date | string | null | undefined,
  options?: Intl.DateTimeFormatOptions
): string => {
  if (!date) return '';

  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;

    if (isNaN(dateObj.getTime())) {
      return '';
    }

    const defaultOptions: Intl.DateTimeFormatOptions = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    };

    return dateObj.toLocaleDateString(undefined, options || defaultOptions);
  } catch (e) {
    console.error('Error formatting date:', e);
    return '';
  }
};

export const formatBirthday = (dateString: string | null | undefined): string => {
  if (!dateString) return '';

  try {
    const birthdayDate = new Date(dateString);
    if (isNaN(birthdayDate.getTime())) return '';

    const formatted = format(birthdayDate, 'MMMM d');
    const today = new Date();
    const currentYear = today.getFullYear();

    const thisYearBirthday = new Date(dateString);
    thisYearBirthday.setFullYear(currentYear);

    if (thisYearBirthday < today) {
      thisYearBirthday.setFullYear(currentYear + 1);
    }

    const diffTime = thisYearBirthday.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    let daysText = '';
    if (diffDays === 0) {
      daysText = 'Today!';
    } else if (diffDays === 1) {
      daysText = 'Tomorrow!';
    } else {
      daysText = `${diffDays} days`;
    }

    return `${formatted} (${daysText})`;
  } catch (e) {
    console.error('Error formatting birthday:', e);
    return '';
  }
};
