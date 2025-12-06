<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import Chart from 'chart.js/auto'

// --- State ---
const availableFiles = ref([])       
const selectedFile = ref('')         
const tableData = ref([])            
const isLoading = ref(false)

// Pagination
const currentPage = ref(1)
const pageSize = ref(10)

// Preview & Forms
const filePreview = ref('')
const filterField = ref('')
const filterValue = ref('')
const saveFilename = ref('export.json')

// Stats & Chart
const statsReport = ref(null)
const showStats = ref(false)
let chartInstance = null

// Toasts
const toastMsg = ref('')
const toastType = ref('')
const showToast = ref(false)

const API_URL = 'http://127.0.0.1:8000/api'

// --- Computed  ---
const totalPages = computed(() => Math.ceil(tableData.value.length / pageSize.value))
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return tableData.value.slice(start, start + pageSize.value)
})

// --- Helpers ---
function triggerToast(msg, type = 'success') {
    toastMsg.value = msg
    toastType.value = type
    showToast.value = true
    setTimeout(() => showToast.value = false, 3000)
}

function renderChart() {
    if (chartInstance) chartInstance.destroy()
    const ctx = document.getElementById('statsChart')
    if (!ctx) return

    const firstField = Object.keys(statsReport.value)[0]
    const info = statsReport.value[firstField]

    chartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Valide', 'Null'],
            datasets: [{
                data: [info.non_null_count, info.null_count],
                backgroundColor: ['#10b981', '#ef4444'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { color: '#aaa', font: { size: 10 } } }
            }
        }
    })
}

// --- API ---
async function apiCall(endpoint, payload = null, method = 'POST') {
  isLoading.value = true
  try {
    const options = { method, headers: { 'Content-Type': 'application/json' }}
    if (payload) options.body = JSON.stringify(payload)
    
    const response = await fetch(`${API_URL}/${endpoint}/`, options)
    const data = await response.json()
    
    if (data.status === 'error') throw new Error(data.message)
    return data
  } catch (e) {
    triggerToast(e.message, 'error')
    console.error(e)
    return null
  } finally {
    isLoading.value = false
  }
}

// --- Actions ---
async function fetchFiles() {
  const res = await apiCall('files', null, 'GET')
  if (res && res.files) {
    availableFiles.value = res.files
    if (res.files.length > 0) { selectedFile.value = res.files[0]; getPreview() }
  }
}

async function getPreview() {
    if (!selectedFile.value) return
    filePreview.value = "Chargement..."
    const res = await apiCall('preview', { path: selectedFile.value })
    if (res) filePreview.value = res.preview
}

async function loadData() {
  if (!selectedFile.value) return
  showStats.value = false
  const res = await apiCall('load', { path: selectedFile.value })
  if (res) { 
      tableData.value = res.data
      currentPage.value = 1
      triggerToast(`${res.count} lignes chargées`, 'success')
  }
}

async function applyFilter() {
  const res = await apiCall('filter', { field: filterField.value, value: filterValue.value })
  if (res) {
      tableData.value = res.data
      currentPage.value = 1
      triggerToast('Filtre appliqué', 'info')
  }
}

async function sortCol(colName) {
  const res = await apiCall('sort', { field: colName })
  if (res) tableData.value = res.data
}

async function getStats() {
  const res = await apiCall('stats', null, 'GET')
  if (res) {
    statsReport.value = res.report
    showStats.value = true
    nextTick(() => renderChart())
  }
}

async function saveFile() {
  const res = await apiCall('save', { path: saveFilename.value })
  if (res) triggerToast(`Sauvegardé : ${res.path}`, 'success')
}

// Pagination Controls
function changePage(delta) {
    const newVal = currentPage.value + delta
    if (newVal >= 1 && newVal <= totalPages.value) currentPage.value = newVal
}

onMounted(() => fetchFiles())
</script>

<template>
  <div class="viewer-container">
    
    <div class="top-bar">
        <div class="brand"><h1>Data<span class="highlight">Filter</span></h1></div>
        <div v-if="isLoading" class="loader"></div>
    </div>
    
    <div class="dashboard-grid">
      
      <div class="sidebar">
        
        <div class="card control-card">
            <div class="card-header">
                <svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                <h3>Fichier Source</h3>
            </div>
            <div class="card-body">
                <select v-model="selectedFile" @change="getPreview" class="input-normal">
                    <option v-for="f in availableFiles" :key="f" :value="f">{{ f }}</option>
                </select>
                <button @click="loadData" class="btn btn-primary full-width">Charger</button>
            </div>
            <div v-if="filePreview" class="preview-mini">
                <div class="preview-label">Aperçu</div>
                <pre>{{ filePreview }}</pre>
            </div>
        </div>

        <div class="card control-card">
            <div class="card-header">
                <svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <h3>Filtres</h3>
            </div>
            <div class="card-body">
                <input v-model="filterField" placeholder="Colonne (ex: age)" class="input-normal input-dark" />
                <input v-model="filterValue" placeholder="Valeur (ex: 25)" class="input-normal input-dark" />
                <button @click="applyFilter" class="btn btn-secondary full-width">Appliquer</button>
            </div>
        </div>

        <div class="card control-card">
            <div class="card-header">
                <svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
                <h3>Actions</h3>
            </div>
            <div class="card-body tools-body">
                <button @click="getStats" class="btn btn-info full-width">
                    <svg class="icon-btn" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 20V10"></path><path d="M12 20V4"></path><path d="M6 20v-6"></path></svg> Stats
                </button>
                <div class="divider"></div>
                <div class="save-group">
                    <input v-model="saveFilename" placeholder="Nom fichier" class="input-normal input-dark" />
                    <button @click="saveFile" class="btn btn-success">
                        <svg class="icon-btn-only" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
                    </button>
                </div>
            </div>
        </div>

      </div>

      <div class="main-content">
        
        <transition name="fade">
            <div v-if="showStats && statsReport" class="card stats-panel">
                <div class="card-header flex-between">
                    <h3>Analyse & Graphique</h3>
                    <button class="btn-icon" @click="showStats = false">✕</button>
                </div>
                <div class="stats-content-wrapper">
                    <div class="chart-container">
                        <canvas id="statsChart"></canvas>
                    </div>
                    <div class="stats-grid">
                        <div v-for="(info, field) in statsReport" :key="field" class="stat-item">
                            <div class="stat-title">{{ field }}</div>
                            <div class="stat-metrics">
                                <span class="metric valid">{{ info.non_null_count }} <small>ok</small></span>
                                <span class="metric null" v-if="info.null_count > 0">{{ info.null_count }} <small>null</small></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </transition>

        <div class="card table-card">
            <div v-if="tableData.length" class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th v-for="(val, key) in tableData[0]" :key="key" @click="sortCol(key)">
                                <div class="th-content">{{ key }} <span class="sort-arrow">↕</span></div>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(row, i) in paginatedData" :key="i">
                            <td v-for="(val, key) in row" :key="key">
                                <span class="cell-content">{{ typeof val === 'object' ? JSON.stringify(val) : val }}</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else class="empty-state">
                <div class="empty-icon">Select</div>
                <p>Aucune donnée chargée.</p>
            </div>

            <div v-if="tableData.length > 0" class="pagination-footer">
                <span class="page-info">Page {{ currentPage }} / {{ totalPages }} ({{ tableData.length }} lignes)</span>
                <div class="page-controls">
                    <button @click="changePage(-1)" :disabled="currentPage === 1" class="btn btn-sm btn-secondary">Précédent</button>
                    <button @click="changePage(1)" :disabled="currentPage === totalPages" class="btn btn-sm btn-secondary">Suivant</button>
                </div>
            </div>
        </div>

      </div>
    </div>

<transition name="slide-up">
        <div v-if="showToast" class="app-toast" :class="toastType">
            {{ toastMsg }}
        </div>
    </transition>

  </div>
</template>

<style scoped>
.viewer-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.brand h1 {
    font-size: 1.8rem;
    margin: 0;
    letter-spacing: -1px;
}

.highlight {
    color: #646cff;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 25px;
    align-items: start;
}

.sidebar {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.main-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.card {
    background: #1e1e1e;
    border-radius: 12px;
    border: 1px solid #333;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.card-header {
    padding: 15px 20px;
    border-bottom: 1px solid #333;
    background: rgba(255, 255, 255, 0.02);
    display: flex;
    align-items: center;
    gap: 10px;
}

.card-header h3 {
    margin: 0;
    font-size: 0.9rem;
    font-weight: 600;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.card-body {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.icon {
    color: #646cff;
    opacity: 0.9;
}

.input-normal {
    width: 100%;
    padding: 10px 12px;
    background: #2a2a2a;
    border: 1px solid #444;
    border-radius: 6px;
    color: white;
    font-family: inherit;
    font-size: 0.9rem;
    transition: border-color 0.2s;
    box-sizing: border-box;
}

.input-normal:focus {
    outline: none;
    border-color: #646cff;
}

.input-dark {
    background: #151515;
}

.btn {
    border: none;
    padding: 10px 16px;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.9rem;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
}

.btn:hover {
    transform: translateY(-1px);
    filter: brightness(110%);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

.full-width {
    width: 100%;
}

.btn-primary {
    background: #646cff;
    color: white;
}

.btn-secondary {
    background: #333;
    color: white;
    border: 1px solid #444;
}

.btn-info {
    background: #0ea5e9;
    color: white;
}

.btn-success {
    background: #10b981;
    color: white;
    padding: 10px;
}

.btn-sm {
    padding: 5px 12px;
    font-size: 0.8rem;
}

.btn-icon {
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
}

.preview-mini {
    margin-top: 0;
    background: #000;
    border-top: 1px solid #333;
    padding: 15px;
}

.preview-label {
    font-size: 0.7rem;
    color: #666;
    margin-bottom: 5px;
    text-transform: uppercase;
}

.preview-mini pre {
    margin: 0;
    font-family: monospace;
    font-size: 0.75rem;
    color: #a5b4fc;
    white-space: pre-wrap;
    max-height: 150px;
    overflow-y: auto;
}

.divider {
    height: 1px;
    background: #333;
    margin: 5px 0;
}

.save-group {
    display: flex;
    gap: 8px;
}

.stats-panel {
    border-color: #646cff;
}

.flex-between {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.stats-content-wrapper {
    display: flex;
    gap: 20px;
    padding: 20px;
}

.chart-container {
    flex: 0 0 150px;
    height: 150px;
    position: relative;
}

.stats-grid {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 10px;
    align-content: flex-start;
}

.stat-item {
    background: rgba(255, 255, 255, 0.03);
    padding: 10px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.stat-title {
    color: #aaa;
    font-size: 0.8rem;
    margin-bottom: 5px;
}

.metric {
    font-size: 1rem;
    font-weight: 700;
    display: block;
}

.metric.valid {
    color: #10b981;
}

.metric.null {
    color: #ef4444;
    font-size: 0.85rem;
}

.table-card {
    min-height: 400px;
    display: flex;
    flex-direction: column;
}

.table-responsive {
    overflow-x: auto;
    flex: 1;
}

table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}

th {
    background: #1a1a1a;
    padding: 15px;
    text-align: left;
    font-weight: 600;
    color: #aaa;
    border-bottom: 1px solid #333;
    position: sticky;
    top: 0;
    white-space: nowrap;
}

th:hover {
    color: white;
    background: #222;
    cursor: pointer;
}

td {
    padding: 12px 15px;
    border-bottom: 1px solid #2a2a2a;
    color: #ddd;
    font-size: 0.9rem;
    white-space: nowrap;
}

tr:hover td {
    background: rgba(255, 255, 255, 0.03);
}

.th-content {
    display: flex;
    justify-content: space-between;
    gap: 10px;
}

.pagination-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-top: 1px solid #333;
    background: #1a1a1a;
}

.page-info {
    font-size: 0.85rem;
    color: #aaa;
}

.page-controls {
    display: flex;
    gap: 10px;
}

.empty-state {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #aaa;
    opacity: 0.5;
    padding: 40px;
}

.empty-icon {
    font-size: 4rem;
    margin-bottom: 20px;
    font-weight: 900;
    opacity: 0.1;
}

.loader {
    width: 24px;
    height: 24px;
    border: 3px solid #333;
    border-bottom-color: #646cff;
    border-radius: 50%;
    display: inline-block;
    animation: rotation 1s linear infinite;
}

@keyframes rotation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
}
.app-toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 12px 20px;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    z-index: 100;
}

.app-toast.success {
    background: #10b981;
}

.app-toast.error {
    background: #ef4444;
}

.app-toast.info {
    background: #3b82f6;
}

.slide-up-enter-active,
.slide-up-leave-active {
    transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
    transform: translateY(20px);
    opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>