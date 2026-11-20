'use strict';
const filters = [...document.querySelectorAll('[data-filter]')];
const jobs = [...document.querySelectorAll('.job')];
document.querySelector('.filters').hidden = false;
function filterJobs(category) {
  filters.forEach(button => {
    const active = button.dataset.filter === category;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  let count = 0;
  jobs.forEach(job => {
    job.hidden = category !== 'all' && job.dataset.category !== category;
    if (!job.hidden) count++;
  });
  document.getElementById('filter-status').textContent = `Показано вакансий: ${count}`;
}
filters.forEach(button => button.addEventListener('click', () => filterJobs(button.dataset.filter)));
function openLinkedJob() {
  let id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
  const job = jobs.find(item => item.id === id);
  if (!job) return;
  filterJobs('all');
  job.open = true;
  requestAnimationFrame(() => job.scrollIntoView({block: 'start', behavior: 'instant'}));
}
window.addEventListener('hashchange', openLinkedJob);
document.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener('click', () => {
  if (link.hash === '#vacancies') filterJobs('all');
  if (link.hash === location.hash) openLinkedJob();
}));
openLinkedJob();
