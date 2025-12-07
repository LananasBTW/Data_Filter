<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import SidebarControls from './dashboard/SidebarControls.vue'
import StatsPanel from './dashboard/StatsPanel.vue'
import DataTable from './dashboard/DataTable.vue'

// --- CONFIG & STATE ---
const API_URL = 'https://api.ptitgourmand.uk/datafilter'

const availableFiles = ref([])       
const tableData = ref([])            
const isLoading = ref(false)
const previewContent = ref('')
const statsReport = ref(null)
const showStats = ref(false)

// --- PAGINATION STATE ---
const currentPage = ref(1)
const pageSize = ref(10)

const totalPages = computed(() => {
    if (!tableData.value.length) return 0
    return Math.ceil(tableData.value.length / pageSize.value)
})

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return tableData.value.slice(start, start + pageSize.value)
})

// --- TOASTS ---
const toastMsg = ref('')
const toastType = ref('')
const showToast = ref(false)

function triggerToast(msg, type = 'success') {
    toastMsg.value = msg
    toastType.value = type
    showToast.value = true
    setTimeout(() => showToast.value = false, 3000)
}

// --- API HELPER ---
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

// --- HANDLERS (LOGIQUE MÉTIER) ---

async function fetchFiles() {
  const res = await apiCall('files', null, 'GET')
  if (res && res.files) {
    availableFiles.value = res.files
  }
}

async function handleLoadFile(filename) {
    const res = await apiCall('preview', { path: filename })
    if (res) previewContent.value = res.preview
}

async function handleLoadData(filename) {
  if (!filename) return
  // NOTE : On ne met plus showStats = false ici pour garder l'affichage si déjà ouvert
  
  const res = await apiCall('load', { path: filename })
  if (res) { 
      tableData.value = res.data
      currentPage.value = 1
      triggerToast(`${res.count} lignes chargées`, 'success')
      
      await handleStats(false) 
  }
}

async function handleFilter({ field, value }) {
  const res = await apiCall('filter', { field, value })
  if (res) {
      tableData.value = res.data
      currentPage.value = 1
      triggerToast('Filtre appliqué', 'info')
      
      await handleStats(false)
  }
}

async function handleStats(forceFocus = false) {
  const res = await apiCall('stats', null, 'GET')
  if (res) {
    statsReport.value = res.report
    showStats.value = true
    
    if (forceFocus === true) {
        nextTick(() => {
            const statsElement = document.querySelector('.stats-panel')
            if (statsElement) {
                statsElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
            }
        })
    }
  }
}

async function handleSave(filename) {
    const res = await apiCall('save', { path: filename })
    if (res) triggerToast(`Sauvegardé : ${res.path}`, 'success')
}

async function handleSort(colName) {
  const res = await apiCall('sort', { field: colName })
  if (res) tableData.value = res.data
}

function handlePageChange(delta) {
    const newVal = currentPage.value + delta
    if (newVal >= 1 && newVal <= totalPages.value) currentPage.value = newVal
}

onMounted(() => {
    fetchFiles()
})
</script>

<template>
  <div class="viewer-container">
    
    <div class="top-bar">
        <div class="brand"><h1>Data<span class="highlight">Filter</span></h1></div>
        <div v-if="isLoading" class="loader"></div>
    </div>
    
    <div class="dashboard-grid">
      
        <SidebarControls 
        :files="availableFiles"
        :is-loading="isLoading"
        :preview-text="previewContent"
        @load-file="handleLoadFile"
        @load-data="handleLoadData"
        @apply-filter="handleFilter"
        @get-stats="handleStats(true)"   @save-file="handleSave"
        />

        <div class="main-content">

            <DataTable 
                :data="paginatedData"
                :current-page="currentPage"
                :total-pages="totalPages"
                @sort="handleSort"
                @page-change="handlePageChange"
            />
            
            <transition name="fade">
                <StatsPanel 
                    v-if="showStats && statsReport" 
                    :report="statsReport" 
                    @close="showStats = false" 
                />
            </transition>

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
    font-family: 'Inter', sans-serif;
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
    color: white;
}

.highlight { color: #646cff; }

.dashboard-grid {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 25px;
    align-items: start;
}

.main-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* LOADER */
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
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* TOAST */
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
.app-toast.success { background: #10b981; }
.app-toast.error { background: #ef4444; }
.app-toast.info { background: #3b82f6; }

/* TRANSITIONS */
.slide-up-enter-active,
.slide-up-leave-active { transition: all 0.3s ease; }
.slide-up-enter-from,
.slide-up-leave-to { transform: translateY(20px); opacity: 0; }

.fade-enter-active,
.fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from,
.fade-leave-to { opacity: 0; }
</style>