// CelebrateAI - Frontend Controller & State Management

let currentEvent = null;
let activeTab = 'ideas';
let timelineSubTab = 'milestones';
let budgetChartInstance = null;
let chatHistory = [];
let userApiKey = localStorage.getItem('celebrate_ai_gemini_key') || '';

// Initialize application on DOM ready
document.addEventListener('DOMContentLoaded', async () => {
  if (window.lucide) {
    lucide.createIcons();
  }
  updateApiKeyBadge();

  // Load saved event from LocalStorage, or load default sample
  const saved = localStorage.getItem('celebrate_ai_current_event');
  if (saved) {
    try {
      currentEvent = JSON.parse(saved);
      renderAll();
    } catch (e) {
      console.warn("Failed to parse cached event, loading sample wedding");
      await loadSamplePreset('wedding');
    }
  } else {
    await loadSamplePreset('wedding');
  }
});

// Format currency
function formatCurrency(amount, currency = 'USD') {
  const symbols = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'INR': '₹',
    'CAD': '$',
    'AUD': '$'
  };
  const sym = symbols[currency] || (currency + ' ');
  return `${sym}${Number(amount || 0).toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 2 })}`;
}

// Render everything based on currentEvent
function renderAll() {
  if (!currentEvent) return;

  renderHeaderAndStats();
  renderIdeasTab();
  renderBudgetTab();
  renderTimelineTab();
  renderVendorsTab();

  // Save to localStorage
  localStorage.setItem('celebrate_ai_current_event', JSON.stringify(currentEvent));

  if (window.lucide) {
    lucide.createIcons();
  }
}

// -------------------------------------------------------------
// Header & Overview Stats
// -------------------------------------------------------------
function renderHeaderAndStats() {
  const ev = currentEvent;
  document.getElementById('event-title').textContent = ev.title || "Untitled Celebration";
  document.getElementById('event-type-text').textContent = (ev.eventType || "Event").toUpperCase();
  
  const iconMap = {
    'wedding': '💍',
    'birthday': '🎂',
    'community': '🎪',
    'other': '✨'
  };
  document.getElementById('badge-event-icon').textContent = iconMap[ev.eventType] || '✨';

  document.getElementById('event-date-text').textContent = ev.date || "Date to be confirmed";
  document.getElementById('event-location-text').textContent = ev.location || "Location pending";
  document.getElementById('event-vibe-preview').textContent = ev.vibeAndStyle || "Custom designed gathering";

  // Guest stats
  const guests = ev.guestCount || 0;
  document.getElementById('stat-guests').textContent = guests;

  // Budget stats
  const totalBudget = ev.totalBudget || 0;
  document.getElementById('stat-budget').textContent = formatCurrency(totalBudget, ev.currency);
  const perGuest = guests > 0 ? totalBudget / guests : 0;
  document.getElementById('stat-per-guest').textContent = `~${formatCurrency(perGuest, ev.currency)} / guest`;

  // Milestone stats
  const milestones = ev.timeline || [];
  const completedMilestones = milestones.filter(m => m.completed).length;
  const milestonePct = milestones.length > 0 ? Math.round((completedMilestones / milestones.length) * 100) : 0;
  document.getElementById('stat-timeline').textContent = `${completedMilestones}/${milestones.length}`;
  document.getElementById('stat-timeline-pct').textContent = `${milestonePct}% Completed`;
  document.getElementById('milestone-progress-text').textContent = `${milestonePct}% Complete`;

  // Vendor stats
  const vendors = ev.vendorChecklist || [];
  const bookedVendors = vendors.filter(v => v.status === 'booked' || v.status === 'completed').length;
  let totalTasks = 0;
  let doneTasks = 0;
  vendors.forEach(v => {
    (v.checklist || []).forEach(t => {
      totalTasks++;
      if (t.completed) doneTasks++;
    });
  });
  document.getElementById('stat-vendors').textContent = `${bookedVendors}/${vendors.length}`;
  document.getElementById('stat-vendors-tasks').textContent = `${doneTasks}/${totalTasks} Tasks Done`;
}

// -------------------------------------------------------------
// TAB 1: AI Ideas & Concepts
// -------------------------------------------------------------
function renderIdeasTab() {
  const ideas = currentEvent.ideas || {};
  document.getElementById('theme-title').textContent = ideas.themeTitle || "Tailored Celebration Concept";
  document.getElementById('theme-concept').textContent = ideas.themeConcept || "An unforgettable experience designed for your guests.";

  // Palette
  const paletteBox = document.getElementById('palette-container');
  paletteBox.innerHTML = '';
  (ideas.colorPalette || []).forEach(color => {
    const swatch = document.createElement('div');
    swatch.className = "group relative flex flex-col items-center cursor-pointer";
    swatch.onclick = () => {
      navigator.clipboard.writeText(color.hex);
      showToast(`Copied ${color.hex}`);
    };
    swatch.innerHTML = `
      <div class="w-9 h-9 rounded-xl border border-white/20 shadow-sm transition transform group-hover:scale-110" style="background-color: ${color.hex};"></div>
      <span class="text-[10px] text-slate-400 mt-1 truncate max-w-[56px] text-center">${color.name}</span>
      <div class="hidden group-hover:block absolute -top-8 bg-slate-900 border border-slate-700 text-white text-[10px] py-0.5 px-1.5 rounded shadow pointer-events-none z-20 whitespace-nowrap">
        ${color.hex} (Click to copy)
      </div>
    `;
    paletteBox.appendChild(swatch);
  });

  // Food & Drinks
  renderSimpleList('list-food-drinks', ideas.signatureFoodAndDrinks || [], 'utensils');
  // Activities
  renderSimpleList('list-activities', ideas.activitiesAndEntertainment || [], 'music');
  // Surprises
  renderSimpleList('list-surprises', ideas.surpriseElements || [], 'sparkles');
  // Decor
  renderSimpleList('list-decor', ideas.decorAndAtmosphere || [], 'flower');

  // Moodboard Prompt
  document.getElementById('moodboard-prompt-box').textContent = ideas.moodboardPrompt || "Warm cinematic lighting, photorealistic details...";
}

function renderSimpleList(elementId, items, iconName) {
  const container = document.getElementById(elementId);
  container.innerHTML = '';
  if (!items || items.length === 0) {
    container.innerHTML = `<li class="text-xs text-slate-500 italic">No items listed yet.</li>`;
    return;
  }
  items.forEach(text => {
    const li = document.createElement('li');
    li.className = "flex items-start gap-2.5";
    li.innerHTML = `
      <span class="mt-0.5 text-rose-400 text-xs shrink-0">✦</span>
      <span class="text-xs text-slate-300 leading-relaxed">${text}</span>
    `;
    container.appendChild(li);
  });
}

function copyMoodboardPrompt() {
  const text = document.getElementById('moodboard-prompt-box').textContent;
  navigator.clipboard.writeText(text);
  showToast("Moodboard prompt copied to clipboard!");
}

// -------------------------------------------------------------
// TAB 2: Budget Maestro
// -------------------------------------------------------------
function renderBudgetTab() {
  const ev = currentEvent;
  const items = ev.budgetBreakdown || [];

  let totalAllocated = 0;
  let totalActual = 0;
  let totalPaid = 0;
  const categoryMap = {};

  items.forEach(item => {
    const est = Number(item.estimatedCost) || 0;
    const act = Number(item.actualCost) || 0;
    const paid = Number(item.paidAmount) || 0;

    totalAllocated += est;
    totalActual += (act > 0 ? act : est);
    totalPaid += paid;

    const cat = item.category || 'Other';
    categoryMap[cat] = (categoryMap[cat] || 0) + (act > 0 ? act : est);
  });

  const totalBudget = ev.totalBudget || 0;
  const cushion = totalBudget - totalActual;

  document.getElementById('budget-allocated-label').textContent = formatCurrency(totalAllocated, ev.currency);
  document.getElementById('budget-contracted-label').textContent = formatCurrency(totalActual, ev.currency);
  document.getElementById('budget-paid-label').textContent = formatCurrency(totalPaid, ev.currency);
  
  const cushionLabel = document.getElementById('budget-cushion-label');
  cushionLabel.textContent = formatCurrency(cushion, ev.currency);
  if (cushion < 0) {
    cushionLabel.className = "text-rose-400 font-bold";
    cushionLabel.textContent += " (Over budget!)";
  } else {
    cushionLabel.className = "text-emerald-400 font-semibold";
  }

  // Progress Bar
  const spentPct = totalBudget > 0 ? Math.min(100, Math.round((totalActual / totalBudget) * 100)) : 0;
  const bar = document.getElementById('budget-progress-bar');
  bar.style.width = `${spentPct}%`;
  if (cushion < 0) {
    bar.className = "bg-rose-500 h-full rounded-full transition-all duration-500";
  } else {
    bar.className = "bg-gradient-to-r from-rose-500 to-amber-400 h-full rounded-full transition-all duration-500";
  }

  // Category Pills
  const chipsContainer = document.getElementById('budget-category-chips');
  chipsContainer.innerHTML = '';
  Object.keys(categoryMap).forEach(cat => {
    const catTotal = categoryMap[cat];
    const catPct = totalActual > 0 ? Math.round((catTotal / totalActual) * 100) : 0;
    const chip = document.createElement('div');
    chip.className = "text-xs px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 flex items-center gap-1.5";
    chip.innerHTML = `
      <span class="w-2 h-2 rounded-full bg-rose-400"></span>
      <span class="font-medium">${cat}:</span>
      <span class="text-white font-semibold">${formatCurrency(catTotal, ev.currency)}</span>
      <span class="text-[10px] text-slate-500">(${catPct}%)</span>
    `;
    chipsContainer.appendChild(chip);
  });

  // Expense Table
  const tableBody = document.getElementById('budget-table-body');
  tableBody.innerHTML = '';
  document.getElementById('expense-count-label').textContent = `${items.length} items listed`;

  items.forEach((item, index) => {
    const tr = document.createElement('tr');
    tr.className = "hover:bg-slate-900/40 transition";
    
    const statusBadges = {
      'planned': `<span class="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">Planned</span>`,
      'booked': `<span class="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/30">Booked</span>`,
      'paid': `<span class="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">Paid</span>`
    };

    tr.innerHTML = `
      <td class="py-3 px-4 font-medium text-slate-200 text-xs">${item.category}</td>
      <td class="py-3 px-4">
        <div class="text-sm font-semibold text-white">${item.item}</div>
        ${item.notes ? `<div class="text-[11px] text-slate-400 mt-0.5">${item.notes}</div>` : ''}
      </td>
      <td class="py-3 px-4 text-right text-xs text-slate-300">${formatCurrency(item.estimatedCost, ev.currency)}</td>
      <td class="py-3 px-4 text-right text-xs font-semibold ${item.actualCost > item.estimatedCost ? 'text-rose-400' : 'text-slate-200'}">
        ${formatCurrency(item.actualCost, ev.currency)}
      </td>
      <td class="py-3 px-4 text-right text-xs text-emerald-400 font-semibold">${formatCurrency(item.paidAmount, ev.currency)}</td>
      <td class="py-3 px-4 text-center">
        <button onclick="toggleBudgetItemStatus(${index})" title="Click to cycle status: Planned -> Booked -> Paid">
          ${statusBadges[item.status] || statusBadges['planned']}
        </button>
      </td>
      <td class="py-3 px-4 text-center">
        <button onclick="deleteBudgetItem(${index})" class="text-slate-500 hover:text-rose-400 transition p-1">
          <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
        </button>
      </td>
    `;
    tableBody.appendChild(tr);
  });

  // Render Doughnut Chart
  renderBudgetChart(categoryMap, ev.currency);
}

function renderBudgetChart(categoryMap, currency) {
  const ctx = document.getElementById('budgetChart');
  if (!ctx) return;

  if (budgetChartInstance) {
    budgetChartInstance.destroy();
  }

  const labels = Object.keys(categoryMap);
  const data = Object.values(categoryMap);
  const backgroundColors = [
    '#f43f5e', '#fb923c', '#eab308', '#10b981', '#06b6d4', '#6366f1', '#a855f7', '#ec4899', '#64748b'
  ];

  budgetChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: backgroundColors.slice(0, labels.length),
        borderWidth: 2,
        borderColor: '#0f172a'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const val = context.raw || 0;
              return ` ${context.label}: ${formatCurrency(val, currency)}`;
            }
          }
        }
      },
      cutout: '70%'
    }
  });

  // Legend list
  const legendBox = document.getElementById('budget-chart-legend');
  legendBox.innerHTML = '';
  labels.forEach((label, i) => {
    const span = document.createElement('span');
    span.className = "flex items-center gap-1.5";
    span.innerHTML = `
      <span class="w-2 h-2 rounded-full" style="background-color: ${backgroundColors[i % backgroundColors.length]};"></span>
      <span class="text-[11px] text-slate-300">${label}</span>
    `;
    legendBox.appendChild(span);
  });
}

function toggleBudgetItemStatus(index) {
  const statuses = ['planned', 'booked', 'paid'];
  const current = currentEvent.budgetBreakdown[index].status || 'planned';
  const next = statuses[(statuses.indexOf(current) + 1) % statuses.length];
  currentEvent.budgetBreakdown[index].status = next;
  renderAll();
  if (next === 'paid') {
    confetti({ particleCount: 30, spread: 60, origin: { y: 0.8 } });
  }
}

function deleteBudgetItem(index) {
  currentEvent.budgetBreakdown.splice(index, 1);
  renderAll();
  showToast("Expense removed.");
}

// -------------------------------------------------------------
// TAB 3: Timeline & Run-of-Show
// -------------------------------------------------------------
function renderTimelineTab() {
  const ev = currentEvent;
  const milestones = ev.timeline || [];
  const schedule = ev.dayOfSchedule || [];

  // Render Milestones
  const mContainer = document.getElementById('milestones-container');
  mContainer.innerHTML = '';
  milestones.forEach((m, idx) => {
    const div = document.createElement('div');
    div.className = "relative group";
    div.innerHTML = `
      <!-- Timeline Node Circle -->
      <div class="absolute -left-[31px] top-1.5 w-5 h-5 rounded-full border-2 ${m.completed ? 'bg-emerald-500 border-emerald-400' : 'bg-slate-900 border-slate-600'} flex items-center justify-center cursor-pointer transition" onclick="toggleMilestone(${idx})">
        ${m.completed ? '<i data-lucide="check" class="w-3 h-3 text-slate-950 font-bold"></i>' : ''}
      </div>

      <div class="glass-card p-4 rounded-xl border border-slate-800/80 hover:border-slate-700 transition">
        <div class="flex items-start justify-between gap-4">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-slate-800 text-rose-300 border border-slate-700">
                ${m.phase}
              </span>
              <span class="text-[10px] text-slate-500">${m.category || 'General'}</span>
              ${m.dueDate ? `<span class="text-[10px] text-amber-400/90 font-mono">Due: ${m.dueDate}</span>` : ''}
            </div>
            <h4 class="text-sm font-bold ${m.completed ? 'line-through text-slate-400' : 'text-white'}">${m.title}</h4>
            <p class="text-xs text-slate-400 leading-relaxed">${m.description}</p>
          </div>
          <div class="flex items-center gap-2">
            <input type="checkbox" ${m.completed ? 'checked' : ''} onchange="toggleMilestone(${idx})" class="w-4 h-4 rounded border-slate-700 text-rose-500 focus:ring-rose-500 cursor-pointer">
            <button onclick="deleteMilestone(${idx})" class="text-slate-500 hover:text-rose-400 p-1 opacity-0 group-hover:opacity-100 transition">
              <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
            </button>
          </div>
        </div>
      </div>
    `;
    mContainer.appendChild(div);
  });

  // Render Day-of Schedule
  const sContainer = document.getElementById('schedule-table-container');
  sContainer.innerHTML = '';
  schedule.forEach((s, idx) => {
    const card = document.createElement('div');
    card.className = "glass-card p-3.5 rounded-xl border border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:border-slate-700 transition";
    
    card.innerHTML = `
      <div class="flex items-start sm:items-center gap-3">
        <div class="w-20 shrink-0 text-xs font-mono font-bold text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2 py-1 rounded-lg text-center">
          ${s.time}
        </div>
        <div class="space-y-0.5">
          <div class="text-sm font-semibold text-white flex items-center gap-2">
            <span>${s.activity}</span>
            ${s.location ? `<span class="text-[11px] text-slate-400 font-normal">📍 ${s.location}</span>` : ''}
          </div>
          <div class="text-xs text-slate-400 flex items-center gap-3">
            ${s.coordinator ? `<span>👤 <strong class="text-slate-300 font-medium">${s.coordinator}</strong></span>` : ''}
            ${s.notes ? `<span class="italic text-slate-400">${s.notes}</span>` : ''}
          </div>
        </div>
      </div>

      <div class="flex items-center gap-2 self-end sm:self-center">
        <select onchange="updateScheduleStatus(${idx}, this.value)" class="bg-slate-900 border border-slate-800 text-[11px] rounded-lg px-2 py-1 text-slate-300 outline-none">
          <option value="upcoming" ${s.status === 'upcoming' ? 'selected' : ''}>Upcoming</option>
          <option value="ongoing" ${s.status === 'ongoing' ? 'selected' : ''}>Ongoing</option>
          <option value="done" ${s.status === 'done' ? 'selected' : ''}>Completed</option>
        </select>
        <button onclick="deleteScheduleItem(${idx})" class="text-slate-500 hover:text-rose-400 p-1">
          <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
        </button>
      </div>
    `;
    sContainer.appendChild(card);
  });
}

function toggleMilestone(index) {
  const m = currentEvent.timeline[index];
  m.completed = !m.completed;
  if (m.completed) {
    confetti({ particleCount: 50, spread: 70, origin: { y: 0.6 } });
    showToast(`Milestone completed: ${m.title}`);
  }
  renderAll();
}

function deleteMilestone(index) {
  currentEvent.timeline.splice(index, 1);
  renderAll();
  showToast("Milestone removed.");
}

function updateScheduleStatus(index, status) {
  currentEvent.dayOfSchedule[index].status = status;
  if (status === 'done') {
    confetti({ particleCount: 25, spread: 50, origin: { y: 0.7 } });
  }
  renderAll();
}

function deleteScheduleItem(index) {
  currentEvent.dayOfSchedule.splice(index, 1);
  renderAll();
  showToast("Schedule item removed.");
}

function switchTimelineSubTab(subTab) {
  timelineSubTab = subTab;
  const mBtn = document.getElementById('subtab-milestones-btn');
  const sBtn = document.getElementById('subtab-schedule-btn');
  const mView = document.getElementById('timeline-milestones-view');
  const sView = document.getElementById('timeline-schedule-view');
  const addBtn = document.getElementById('btn-add-timeline-item');

  if (subTab === 'milestones') {
    mBtn.className = "px-4 py-2 rounded-lg text-xs font-semibold bg-rose-500 text-white transition";
    sBtn.className = "px-4 py-2 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition";
    mView.classList.remove('hidden');
    sView.classList.add('hidden');
    addBtn.innerHTML = `<i data-lucide="plus" class="w-4 h-4"></i> Add Milestone`;
    addBtn.setAttribute('onclick', 'openAddTimelineModal()');
  } else {
    sBtn.className = "px-4 py-2 rounded-lg text-xs font-semibold bg-rose-500 text-white transition";
    mBtn.className = "px-4 py-2 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition";
    sView.classList.remove('hidden');
    mView.classList.add('hidden');
    addBtn.innerHTML = `<i data-lucide="plus" class="w-4 h-4"></i> Add Cue`;
    addBtn.setAttribute('onclick', 'openAddScheduleModal()');
  }
  if (window.lucide) lucide.createIcons();
}

// -------------------------------------------------------------
// TAB 4: Vendor Checklists & CRM
// -------------------------------------------------------------
function renderVendorsTab() {
  const ev = currentEvent;
  const vendors = ev.vendorChecklist || [];
  const grid = document.getElementById('vendors-grid');
  grid.innerHTML = '';

  vendors.forEach((v, vIndex) => {
    const card = document.createElement('div');
    card.className = "glass-card rounded-2xl p-5 border border-slate-800 space-y-4 hover:border-slate-700 transition flex flex-col justify-between";

    const statusPills = {
      'researching': `<span class="text-[10px] uppercase font-semibold px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">Researching</span>`,
      'contacted': `<span class="text-[10px] uppercase font-semibold px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/30">Contacted</span>`,
      'quoted': `<span class="text-[10px] uppercase font-semibold px-2.5 py-1 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/30">Quoted</span>`,
      'booked': `<span class="text-[10px] uppercase font-semibold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">Booked</span>`,
      'completed': `<span class="text-[10px] uppercase font-semibold px-2.5 py-1 rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/30">Completed</span>`
    };

    const tasks = v.checklist || [];
    const doneTasks = tasks.filter(t => t.completed).length;
    const taskPct = tasks.length > 0 ? Math.round((doneTasks / tasks.length) * 100) : 0;

    let tasksHtml = '';
    tasks.forEach((t, tIndex) => {
      tasksHtml += `
        <li class="flex items-center justify-between text-xs py-1 text-slate-300">
          <label class="flex items-center gap-2 cursor-pointer select-none">
            <input type="checkbox" ${t.completed ? 'checked' : ''} onchange="toggleVendorTask(${vIndex}, ${tIndex})" class="w-3.5 h-3.5 rounded border-slate-700 text-rose-500 focus:ring-rose-500">
            <span class="${t.completed ? 'line-through text-slate-500' : 'text-slate-300'}">${t.task}</span>
          </label>
          <button onclick="deleteVendorTask(${vIndex}, ${tIndex})" class="text-slate-600 hover:text-rose-400">
            <i data-lucide="x" class="w-3 h-3"></i>
          </button>
        </li>
      `;
    });

    card.innerHTML = `
      <div class="space-y-3">
        <div class="flex items-start justify-between gap-3">
          <div>
            <span class="text-[10px] uppercase font-bold text-rose-400 tracking-wider block">${v.category}</span>
            <h3 class="text-base font-bold text-white">${v.vendorName}</h3>
          </div>
          <button onclick="cycleVendorStatus(${vIndex})" title="Click to cycle status">
            ${statusPills[v.status] || statusPills['researching']}
          </button>
        </div>

        <div class="text-xs text-slate-400 space-y-1">
          ${v.contact ? `<p class="flex items-center gap-1.5"><i data-lucide="mail" class="w-3.5 h-3.5 text-slate-500"></i> ${v.contact}</p>` : ''}
          <p class="flex items-center gap-1.5 font-medium text-slate-200">
            <i data-lucide="tag" class="w-3.5 h-3.5 text-emerald-400"></i>
            Estimated: ${formatCurrency(v.estimatedCost, ev.currency)}
            ${v.contractedCost > 0 ? `| Contracted: <span class="text-emerald-400">${formatCurrency(v.contractedCost, ev.currency)}</span>` : ''}
          </p>
          ${v.notes ? `<p class="text-[11px] text-slate-400 italic bg-slate-900/60 p-2 rounded-lg border border-slate-800">${v.notes}</p>` : ''}
        </div>

        <!-- Task Checklist & Progress -->
        <div class="space-y-2 pt-2 border-t border-slate-800/80">
          <div class="flex justify-between items-center text-[11px]">
            <span class="font-semibold text-slate-300">Deliverables & Tasks</span>
            <span class="text-slate-400">${doneTasks}/${tasks.length} (${taskPct}%)</span>
          </div>
          <div class="w-full bg-slate-900 rounded-full h-1.5 overflow-hidden">
            <div class="bg-rose-500 h-full rounded-full transition-all duration-300" style="width: ${taskPct}%;"></div>
          </div>
          <ul class="space-y-1 divide-y divide-slate-800/40">
            ${tasksHtml || '<li class="text-[11px] text-slate-500 italic py-1">No tasks yet.</li>'}
          </ul>
        </div>
      </div>

      <div class="flex items-center justify-between pt-3 border-t border-slate-800/60 text-xs mt-3">
        <button onclick="openAddTaskToVendorModal(${vIndex})" class="text-xs text-rose-400 hover:text-rose-300 font-medium flex items-center gap-1">
          <i data-lucide="plus" class="w-3.5 h-3.5"></i> Add Task
        </button>
        <button onclick="deleteVendor(${vIndex})" class="text-slate-500 hover:text-rose-400 p-1">
          <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
        </button>
      </div>
    `;
    grid.appendChild(card);
  });
}

function toggleVendorTask(vIndex, tIndex) {
  const task = currentEvent.vendorChecklist[vIndex].checklist[tIndex];
  task.completed = !task.completed;
  if (task.completed) {
    confetti({ particleCount: 20, spread: 45, origin: { y: 0.7 } });
  }
  renderAll();
}

function deleteVendorTask(vIndex, tIndex) {
  currentEvent.vendorChecklist[vIndex].checklist.splice(tIndex, 1);
  renderAll();
}

function cycleVendorStatus(vIndex) {
  const statuses = ['researching', 'contacted', 'quoted', 'booked', 'completed'];
  const current = currentEvent.vendorChecklist[vIndex].status || 'researching';
  const next = statuses[(statuses.indexOf(current) + 1) % statuses.length];
  currentEvent.vendorChecklist[vIndex].status = next;
  renderAll();
  showToast(`Vendor status updated to ${next.toUpperCase()}`);
}

function deleteVendor(vIndex) {
  currentEvent.vendorChecklist.splice(vIndex, 1);
  renderAll();
  showToast("Vendor removed.");
}

// -------------------------------------------------------------
// TAB 5: Interactive Chat (EventGenie AI)
// -------------------------------------------------------------
async function handleChatSubmit(e) {
  if (e) e.preventDefault();
  const input = document.getElementById('chat-input');
  const message = input.value.trim();
  if (!message) return;

  input.value = '';
  appendChatMessage('user', message);

  // Show typing indicator
  const typingId = appendChatTyping();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: message,
        eventContext: currentEvent,
        chatHistory: chatHistory,
        apiKey: userApiKey || null
      })
    });
    const data = await res.json();
    removeChatElement(typingId);

    const reply = data.reply || "I'm here to help with your event planning! What would you like to explore next?";
    appendChatMessage('assistant', reply);
  } catch (err) {
    removeChatElement(typingId);
    appendChatMessage('assistant', "Sorry, I encountered a temporary connection issue. Please try again.");
  }
}

function sendQuickPrompt(promptText) {
  switchTab('chat');
  const input = document.getElementById('chat-input');
  input.value = promptText;
  handleChatSubmit();
}

function appendChatMessage(role, content) {
  chatHistory.push({ role, content });
  const container = document.getElementById('chat-messages');

  const div = document.createElement('div');
  div.className = `flex items-start gap-3 ${role === 'user' ? 'justify-end' : ''}`;

  if (role === 'assistant') {
    div.innerHTML = `
      <div class="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center shrink-0 border border-amber-500/30">
        <i data-lucide="bot" class="w-4 h-4"></i>
      </div>
      <div class="bg-slate-900/90 rounded-2xl p-4 max-w-2xl border border-slate-800 text-sm text-slate-200 leading-relaxed shadow-sm space-y-2">
        ${window.marked ? marked.parse(content) : content}
      </div>
    `;
  } else {
    div.innerHTML = `
      <div class="bg-rose-600 rounded-2xl p-3.5 max-w-xl text-sm text-white leading-relaxed shadow-md">
        ${escapeHtml(content)}
      </div>
      <div class="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-300 flex items-center justify-center shrink-0 border border-rose-500/30">
        <i data-lucide="user" class="w-4 h-4"></i>
      </div>
    `;
  }

  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  if (window.lucide) lucide.createIcons();
}

function appendChatTyping() {
  const container = document.getElementById('chat-messages');
  const id = 'typing-' + Date.now();
  const div = document.createElement('div');
  div.id = id;
  div.className = "flex items-start gap-3";
  div.innerHTML = `
    <div class="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center shrink-0 border border-amber-500/30">
      <i data-lucide="bot" class="w-4 h-4"></i>
    </div>
    <div class="bg-slate-900/90 rounded-2xl px-4 py-3 border border-slate-800 text-xs text-slate-400 flex items-center gap-2">
      <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
      <span class="w-2 h-2 rounded-full bg-rose-400 animate-pulse delay-75"></span>
      <span class="w-2 h-2 rounded-full bg-purple-400 animate-pulse delay-150"></span>
      <span>EventGenie is thinking...</span>
    </div>
  `;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  if (window.lucide) lucide.createIcons();
  return id;
}

function removeChatElement(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function clearChat() {
  chatHistory = [];
  const container = document.getElementById('chat-messages');
  container.innerHTML = `
    <div class="flex items-start gap-3">
      <div class="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center shrink-0 border border-amber-500/30">
        <i data-lucide="sparkles" class="w-4 h-4"></i>
      </div>
      <div class="bg-slate-900/90 rounded-2xl p-4 max-w-2xl border border-slate-800 text-sm text-slate-200 leading-relaxed shadow-sm">
        <p class="font-semibold text-rose-400 mb-1">Chat history refreshed.</p>
        <p class="text-xs text-slate-400">Ask me anything about your active event plan!</p>
      </div>
    </div>
  `;
  if (window.lucide) lucide.createIcons();
}

// -------------------------------------------------------------
// Tab Switching
// -------------------------------------------------------------
function switchTab(tabName) {
  activeTab = tabName;
  const tabs = ['ideas', 'budget', 'timeline', 'vendors', 'chat'];
  tabs.forEach(t => {
    const section = document.getElementById(`tab-${t}`);
    const btn = document.getElementById(`tab-btn-${t}`);
    if (t === tabName) {
      section.classList.remove('hidden');
      btn.className = "tab-btn active px-4 py-2.5 rounded-xl font-medium text-sm flex items-center gap-2 transition bg-rose-500/10 text-rose-400 border border-rose-500/30";
    } else {
      section.classList.add('hidden');
      btn.className = "tab-btn px-4 py-2.5 rounded-xl font-medium text-sm flex items-center gap-2 transition text-slate-400 hover:text-slate-200 hover:bg-slate-900";
    }
  });

  if (tabName === 'budget' && budgetChartInstance) {
    budgetChartInstance.resize();
  }
  if (window.lucide) lucide.createIcons();
}

// -------------------------------------------------------------
// Sample Presets Loader
// -------------------------------------------------------------
async function loadSamplePreset(eventType) {
  showLoading("Loading curated blueprint...", `Fetching realistic blueprint for ${eventType.toUpperCase()}`);
  try {
    const res = await fetch(`/api/samples/${eventType}`);
    if (!res.ok) throw new Error("Preset not found");
    const data = await res.json();
    currentEvent = data;
    renderAll();
    confetti({ particleCount: 40, spread: 60, origin: { y: 0.5 } });
    showToast(`Loaded ${data.title}`);
  } catch (e) {
    showToast("Error loading sample: " + e.message);
  } finally {
    hideLoading();
  }
}

// -------------------------------------------------------------
// Event Wizard Modal & AI Plan Generation
// -------------------------------------------------------------
function openWizardModal() {
  document.getElementById('wizard-modal').classList.remove('hidden');
}

function closeWizardModal() {
  document.getElementById('wizard-modal').classList.add('hidden');
}

function updateWizardDefaults(type) {
  const title = document.getElementById('wiz-title');
  const vibe = document.getElementById('wiz-vibe');
  const budget = document.getElementById('wiz-budget');
  const guests = document.getElementById('wiz-guests');

  if (type === 'wedding') {
    title.value = "Sophia & Julian's Romantic Garden Wedding";
    vibe.value = "Lush botanical florals, champagne tones, candlelit farm tables, acoustic guitar";
    budget.value = "28000";
    guests.value = "90";
  } else if (type === 'birthday') {
    title.value = "Jordan's 30th Rooftop Sunset Social";
    vibe.value = "Retro neon chic, craft cocktails, vinyl DJ, taco bar, polaroid wall";
    budget.value = "4500";
    guests.value = "40";
  } else if (type === 'community') {
    title.value = "Riverside Summer Block Party & Art Fair";
    vibe.value = "Family-friendly, local food trucks, community makers, acoustic stage, eco recycling";
    budget.value = "10000";
    guests.value = "300";
  }
}

function setVibeQuick(text) {
  document.getElementById('wiz-vibe').value = text;
}

async function handleWizardSubmit(e) {
  e.preventDefault();
  closeWizardModal();

  const eventType = document.querySelector('input[name="eventType"]:checked').value;
  const title = document.getElementById('wiz-title').value.trim();
  const guestCount = parseInt(document.getElementById('wiz-guests').value, 10);
  const totalBudget = parseFloat(document.getElementById('wiz-budget').value);
  const currency = document.getElementById('wiz-currency').value;
  const date = document.getElementById('wiz-date').value;
  const location = document.getElementById('wiz-location').value.trim();
  const vibeAndStyle = document.getElementById('wiz-vibe').value.trim();
  const specialRequests = document.getElementById('wiz-special').value.trim();

  showLoading(
    "EventGenie AI is synthesizing your event...",
    "Balancing budgets, crafting timelines, personalizing themes, and building vendor checklists."
  );

  try {
    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        eventType,
        title,
        guestCount,
        totalBudget,
        currency,
        date,
        location,
        vibeAndStyle,
        specialRequests,
        apiKey: userApiKey || null
      })
    });

    if (!res.ok) {
      throw new Error(`Generation failed: ${res.statusText}`);
    }

    const newPlan = await res.json();
    currentEvent = newPlan;
    renderAll();
    switchTab('ideas');

    confetti({
      particleCount: 100,
      spread: 80,
      origin: { y: 0.5 }
    });
    showToast("🎉 Event generated successfully!");
  } catch (err) {
    showToast("Generation error: " + err.message);
  } finally {
    hideLoading();
  }
}

// -------------------------------------------------------------
// Modals for Adding Items (Budget, Timeline, Schedule, Vendor)
// -------------------------------------------------------------
function openItemModal(title, html) {
  document.getElementById('item-modal-title').textContent = title;
  document.getElementById('item-modal-form-container').innerHTML = html;
  document.getElementById('item-modal').classList.remove('hidden');
  if (window.lucide) lucide.createIcons();
}

function closeItemModal() {
  document.getElementById('item-modal').classList.add('hidden');
}

function openAddBudgetModal() {
  const html = `
    <form onsubmit="submitAddBudget(event)" class="space-y-3">
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Category</label>
        <input type="text" id="add-b-cat" placeholder="e.g. Venue, Catering, Music, Decor" required class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Item Description</label>
        <input type="text" id="add-b-item" placeholder="e.g. Acoustic Guitar Duo for Cocktail Hour" required class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Estimated Cost</label>
          <input type="number" id="add-b-est" min="0" step="10" required class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
        </div>
        <div>
          <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Actual / Contracted</label>
          <input type="number" id="add-b-act" min="0" step="10" value="0" class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
        </div>
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Notes</label>
        <input type="text" id="add-b-notes" placeholder="e.g. Deposit required by next Friday" class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div class="flex justify-end gap-2 pt-2">
        <button type="button" onclick="closeItemModal()" class="px-3 py-2 text-xs text-slate-400 hover:text-white">Cancel</button>
        <button type="submit" class="gradient-btn-celebrate px-4 py-2 rounded-lg text-xs font-semibold text-white">Add Expense</button>
      </div>
    </form>
  `;
  openItemModal("Add Budget Item", html);
}

function submitAddBudget(e) {
  e.preventDefault();
  const item = {
    id: "b-" + Date.now(),
    category: document.getElementById('add-b-cat').value.trim(),
    item: document.getElementById('add-b-item').value.trim(),
    estimatedCost: parseFloat(document.getElementById('add-b-est').value) || 0,
    actualCost: parseFloat(document.getElementById('add-b-act').value) || 0,
    paidAmount: 0,
    status: 'planned',
    notes: document.getElementById('add-b-notes').value.trim()
  };
  currentEvent.budgetBreakdown.push(item);
  closeItemModal();
  renderAll();
  showToast("Expense added to budget!");
}

function openAddTimelineModal() {
  const html = `
    <form onsubmit="submitAddMilestone(event)" class="space-y-3">
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Phase</label>
        <input type="text" id="add-t-phase" placeholder="e.g. 6 Months Out, 1 Month Out, Week Of" required class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Milestone Title</label>
        <input type="text" id="add-t-title" placeholder="e.g. Finalize Dinner Menu & Tasting" required class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Description / Action Steps</label>
        <textarea id="add-t-desc" rows="2" placeholder="Specific steps and details" class="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-sm text-white outline-none"></textarea>
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Target Due Date</label>
        <input type="date" id="add-t-date" class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div class="flex justify-end gap-2 pt-2">
        <button type="button" onclick="closeItemModal()" class="px-3 py-2 text-xs text-slate-400 hover:text-white">Cancel</button>
        <button type="submit" class="gradient-btn-celebrate px-4 py-2 rounded-lg text-xs font-semibold text-white">Add Milestone</button>
      </div>
    </form>
  `;
  openItemModal("Add Planning Milestone", html);
}

function submitAddMilestone(e) {
  e.preventDefault();
  const milestone = {
    id: "t-" + Date.now(),
    phase: document.getElementById('add-t-phase').value.trim(),
    title: document.getElementById('add-t-title').value.trim(),
    description: document.getElementById('add-t-desc').value.trim(),
    dueDate: document.getElementById('add-t-date').value,
    completed: false,
    category: "General"
  };
  currentEvent.timeline.push(milestone);
  closeItemModal();
  renderAll();
  showToast("Milestone added!");
}

function openAddScheduleModal() {
  const html = `
    <form onsubmit="submitAddSchedule(event)" class="space-y-3">
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Time</label>
          <input type="text" id="add-s-time" placeholder="e.g. 05:30 PM" required class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
        </div>
        <div>
          <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Location</label>
          <input type="text" id="add-s-loc" placeholder="e.g. Main Courtyard" class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
        </div>
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Activity / Cue</label>
        <input type="text" id="add-s-act" placeholder="e.g. First Dance & Sparkler Cold Fountains" required class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Assigned Coordinator / Role</label>
        <input type="text" id="add-s-coord" placeholder="e.g. DJ Sammy & Wedding Planner" class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Key Notes / Instructions</label>
        <input type="text" id="add-s-notes" placeholder="e.g. Dim chandeliers to 30%" class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div class="flex justify-end gap-2 pt-2">
        <button type="button" onclick="closeItemModal()" class="px-3 py-2 text-xs text-slate-400 hover:text-white">Cancel</button>
        <button type="submit" class="gradient-btn-celebrate px-4 py-2 rounded-lg text-xs font-semibold text-white">Add Schedule Cue</button>
      </div>
    </form>
  `;
  openItemModal("Add Day-of Schedule Cue", html);
}

function submitAddSchedule(e) {
  e.preventDefault();
  const cue = {
    id: "s-" + Date.now(),
    time: document.getElementById('add-s-time').value.trim(),
    activity: document.getElementById('add-s-act').value.trim(),
    location: document.getElementById('add-s-loc').value.trim(),
    coordinator: document.getElementById('add-s-coord').value.trim(),
    notes: document.getElementById('add-s-notes').value.trim(),
    status: 'upcoming'
  };
  currentEvent.dayOfSchedule.push(cue);
  closeItemModal();
  renderAll();
  showToast("Day-of cue added!");
}

function openAddVendorModal() {
  const html = `
    <form onsubmit="submitAddVendor(event)" class="space-y-3">
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Category</label>
        <input type="text" id="add-v-cat" placeholder="e.g. Catering, Photography, Florist, DJ" required class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Vendor / Company Name</label>
        <input type="text" id="add-v-name" placeholder="e.g. Bella Luna Photography" required class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Contact Info</label>
        <input type="text" id="add-v-contact" placeholder="e.g. email@domain.com | (555) 000-1122" class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Estimated Budget</label>
          <input type="number" id="add-v-est" min="0" value="0" class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
        </div>
        <div>
          <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Status</label>
          <select id="add-v-status" class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
            <option value="researching">Researching</option>
            <option value="contacted">Contacted</option>
            <option value="quoted">Quoted</option>
            <option value="booked">Booked</option>
            <option value="completed">Completed</option>
          </select>
        </div>
      </div>
      <div class="flex justify-end gap-2 pt-2">
        <button type="button" onclick="closeItemModal()" class="px-3 py-2 text-xs text-slate-400 hover:text-white">Cancel</button>
        <button type="submit" class="gradient-btn-celebrate px-4 py-2 rounded-lg text-xs font-semibold text-white">Add Vendor</button>
      </div>
    </form>
  `;
  openItemModal("Add Vendor Profile", html);
}

function submitAddVendor(e) {
  e.preventDefault();
  const v = {
    id: "v-" + Date.now(),
    category: document.getElementById('add-v-cat').value.trim(),
    vendorName: document.getElementById('add-v-name').value.trim(),
    contact: document.getElementById('add-v-contact').value.trim(),
    estimatedCost: parseFloat(document.getElementById('add-v-est').value) || 0,
    contractedCost: 0,
    status: document.getElementById('add-v-status').value,
    checklist: [],
    notes: ""
  };
  currentEvent.vendorChecklist.push(v);
  closeItemModal();
  renderAll();
  showToast("Vendor profile added!");
}

function openAddTaskToVendorModal(vIndex) {
  const vendor = currentEvent.vendorChecklist[vIndex];
  const html = `
    <form onsubmit="submitAddTaskToVendor(event, ${vIndex})" class="space-y-3">
      <p class="text-xs text-slate-300">Adding task to <strong class="text-white">${vendor.vendorName}</strong></p>
      <div>
        <label class="block text-xs font-semibold uppercase text-slate-400 mb-1">Task Description</label>
        <input type="text" id="add-vt-desc" placeholder="e.g. Schedule final tasting, sign insurance waiver" required class="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-white outline-none">
      </div>
      <div class="flex justify-end gap-2 pt-2">
        <button type="button" onclick="closeItemModal()" class="px-3 py-2 text-xs text-slate-400 hover:text-white">Cancel</button>
        <button type="submit" class="gradient-btn-celebrate px-4 py-2 rounded-lg text-xs font-semibold text-white">Save Task</button>
      </div>
    </form>
  `;
  openItemModal("Add Deliverable Task", html);
}

function submitAddTaskToVendor(e, vIndex) {
  e.preventDefault();
  const desc = document.getElementById('add-vt-desc').value.trim();
  currentEvent.vendorChecklist[vIndex].checklist.push({
    id: "c-" + Date.now(),
    task: desc,
    completed: false
  });
  closeItemModal();
  renderAll();
  showToast("Deliverable task added!");
}

// -------------------------------------------------------------
// Export & Sharing
// -------------------------------------------------------------
async function openExportModal() {
  document.getElementById('export-modal').classList.remove('hidden');
  try {
    const res = await fetch('/api/export/markdown', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentEvent)
    });
    const data = await res.json();
    document.getElementById('export-preview-area').value = data.markdown || "";
  } catch (e) {
    document.getElementById('export-preview-area').value = JSON.stringify(currentEvent, null, 2);
  }
}

function closeExportModal() {
  document.getElementById('export-modal').classList.add('hidden');
}

function copyMarkdownSummary() {
  const text = document.getElementById('export-preview-area').value;
  navigator.clipboard.writeText(text);
  showToast("Markdown copied to clipboard!");
}

function downloadJsonPlan() {
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(currentEvent, null, 2));
  const dlAnchor = document.createElement('a');
  dlAnchor.setAttribute("href", dataStr);
  dlAnchor.setAttribute("download", `${currentEvent.title.toLowerCase().replace(/[^a-z0-9]/g, '_')}_plan.json`);
  dlAnchor.click();
  showToast("JSON file downloaded!");
}

function printEventBrief() {
  closeExportModal();
  window.print();
}

// -------------------------------------------------------------
// Gemini API Key Management
// -------------------------------------------------------------
function openApiKeyModal() {
  document.getElementById('input-api-key').value = userApiKey;
  document.getElementById('apikey-modal').classList.remove('hidden');
}

function closeApiKeyModal() {
  document.getElementById('apikey-modal').classList.add('hidden');
}

function saveApiKey() {
  const key = document.getElementById('input-api-key').value.trim();
  userApiKey = key;
  if (key) {
    localStorage.setItem('celebrate_ai_gemini_key', key);
    showToast("Gemini API key saved!");
  } else {
    localStorage.removeItem('celebrate_ai_gemini_key');
    showToast("API key removed. Using built-in generator.");
  }
  updateApiKeyBadge();
  closeApiKeyModal();
}

function clearApiKey() {
  userApiKey = '';
  localStorage.removeItem('celebrate_ai_gemini_key');
  document.getElementById('input-api-key').value = '';
  updateApiKeyBadge();
  closeApiKeyModal();
  showToast("API key cleared.");
}

function updateApiKeyBadge() {
  const label = document.getElementById('api-key-label');
  if (userApiKey) {
    label.textContent = "Gemini Key (Active)";
    label.className = "text-emerald-400 font-semibold";
  } else {
    label.textContent = "API Key";
    label.className = "hidden sm:inline";
  }
}

// -------------------------------------------------------------
// UI Utilities (Toast, Loading, String escape)
// -------------------------------------------------------------
function showToast(message) {
  const toast = document.createElement('div');
  toast.className = "fixed bottom-5 right-5 z-50 bg-slate-900 border border-slate-700 text-white text-xs font-medium px-4 py-2.5 rounded-xl shadow-2xl flex items-center gap-2 transform transition-all duration-300 translate-y-2 opacity-0";
  toast.innerHTML = `<i data-lucide="info" class="w-4 h-4 text-rose-400"></i> <span>${escapeHtml(message)}</span>`;
  document.body.appendChild(toast);
  if (window.lucide) lucide.createIcons();

  setTimeout(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  }, 10);

  setTimeout(() => {
    toast.classList.add('translate-y-2', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

function showLoading(title, desc) {
  document.getElementById('loading-title').textContent = title;
  document.getElementById('loading-desc').textContent = desc;
  document.getElementById('loading-overlay').classList.remove('hidden');
}

function hideLoading() {
  document.getElementById('loading-overlay').classList.add('hidden');
}

function escapeHtml(text) {
  const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
  return String(text).replace(/[&<>"']/g, m => map[m]);
}
