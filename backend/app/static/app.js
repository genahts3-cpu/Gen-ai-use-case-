const API_BASE = '/api/usecases';

const form = document.getElementById('usecase-form');
const listEl = document.getElementById('usecase-list');
const template = document.getElementById('usecase-template');
const searchInput = document.getElementById('search');
const searchBtn = document.getElementById('search-btn');
const resetBtn = document.getElementById('reset-btn');

async function fetchUseCases() {
  const res = await fetch(API_BASE);
  return res.json();
}

async function searchUseCases(query) {
  const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
  return res.json();
}

async function createUseCase(data) {
  const res = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return res.json();
}

async function deleteUseCase(id) {
  await fetch(`${API_BASE}/${id}`, { method: 'DELETE' });
}

function renderUseCases(usecases) {
  listEl.innerHTML = '';
  usecases.forEach(uc => {
    const node = template.content.cloneNode(true);
    node.querySelector('.uc-title').textContent = uc.title;
    node.querySelector('.uc-status').textContent = uc.status || 'draft';
    node.querySelector('.uc-description').textContent = uc.description;
    node.querySelector('.uc-industry').textContent = uc.industry;
    node.querySelector('.uc-value').textContent = uc.business_value;
    const tagContainer = node.querySelector('.uc-tags');
    (uc.tags || []).forEach(tag => {
      const span = document.createElement('span');
      span.textContent = tag;
      tagContainer.appendChild(span);
    });
    node.querySelector('.delete-btn').addEventListener('click', async () => {
      await deleteUseCase(uc.id);
      loadUseCases();
    });
    listEl.appendChild(node);
  });
}

async function loadUseCases() {
  const data = await fetchUseCases();
  renderUseCases(data);
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    title: document.getElementById('title').value,
    description: document.getElementById('description').value,
    industry: document.getElementById('industry').value,
    business_value: document.getElementById('business_value').value,
    status: document.getElementById('status').value || 'draft',
    tags: document.getElementById('tags').value
      .split(',')
      .map(t => t.trim())
      .filter(Boolean)
  };
  await createUseCase(payload);
  form.reset();
  loadUseCases();
});

searchBtn.addEventListener('click', async () => {
  const q = searchInput.value.trim();
  if (!q) return;
  const results = await searchUseCases(q);
  renderUseCases(results);
});

resetBtn.addEventListener('click', () => {
  searchInput.value = '';
  loadUseCases();
});

loadUseCases();
