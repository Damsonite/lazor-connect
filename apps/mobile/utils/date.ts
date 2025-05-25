import { format, formatDistance, isToday, isYesterday } from 'date-fns';

/**
 * Formats a date into a human-readable string showing how much time has passed
 * Examples: "just now", "5 minutes ago", "yesterday", "2 weeks ago", "8:50 PM"
 *
 * @param date - The date to format (Date object or ISO string)
 * @returns A human-readable string representing the relative time
 */
export const formatRelativeTime = (date: Date | string): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  const now = new Date();

  // For invalid dates, return empty string
  if (isNaN(dateObj.getTime())) {
    return '';
  }

  // If it's less than a minute ago, show "just now"
  const diffInSeconds = Math.floor((now.getTime() - dateObj.getTime()) / 1000);
  if (diffInSeconds < 60) {
    return 'just now';
  }

  // If it's today, show the time (e.g., "8:50 PM")
  if (isToday(dateObj)) {
    return format(dateObj, 'h:mm a');
  }

  // If it's yesterday, show "yesterday"
  if (isYesterday(dateObj)) {
    return 'yesterday';
  }

  // If it's within the last 7 days, show something like "2 days ago"
  if (diffInSeconds < 7 * 24 * 60 * 60) {
    return formatDistance(dateObj, now, { addSuffix: true });
  }

  // If it's within the current year, show the month and day (e.g., "Apr 15")
  if (dateObj.getFullYear() === now.getFullYear()) {
    return format(dateObj, 'MMM d');
  }

  // For older dates, show the complete date (e.g., "Apr 15, 2023")
  return format(dateObj, 'MMM d, yyyy');
};

/**
 * Formats a time from a date object (e.g., "8:50 PM")
 *
 * @param date - The date to format
 * @returns A formatted time string
 */
export const formatTime = (date: Date | string): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;

  // For invalid dates, return empty string
  if (isNaN(dateObj.getTime())) {
    return '';
  }

  return format(dateObj, 'h:mm a');
};

/**
 * Formats the date for chat message timestamps
 * For today: "8:50 PM"
 * For yesterday: "Yesterday, 8:50 PM"
 * For this week: "Monday, 8:50 PM"
 * Otherwise: "Apr 15, 8:50 PM" or "Apr 15, 2023, 8:50 PM"
 *
 * @param date - The date to format
 * @returns A formatted date string for chat messages
 */
export const formatChatTimestamp = (date: Date | string): string => {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  const now = new Date();

  // For invalid dates, return empty string
  if (isNaN(dateObj.getTime())) {
    return '';
  }

  // Today: Just show time
  if (isToday(dateObj)) {
    return format(dateObj, 'h:mm a');
  }

  // Yesterday
  if (isYesterday(dateObj)) {
    return `Yesterday, ${format(dateObj, 'h:mm a')}`;
  }

  // Within the last 7 days
  const diffInDays = Math.floor((now.getTime() - dateObj.getTime()) / (1000 * 60 * 60 * 24));
  if (diffInDays < 7) {
    return format(dateObj, 'EEEE, h:mm a'); // Day name, time
  }

  // This year
  if (dateObj.getFullYear() === now.getFullYear()) {
    return format(dateObj, 'MMM d, h:mm a');
  }

  // Previous years
  return format(dateObj, 'MMM d, yyyy, h:mm a');
};
