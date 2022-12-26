function calculateDaysBetweenDates(begin, end) {
  const beginDate = new Date(begin);
  const endDate = new Date(end);
  const diff = endDate.getTime() - beginDate.getTime();
  return diff / 1000 / 60 / 60 / 24;
}