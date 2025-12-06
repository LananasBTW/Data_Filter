<script setup>
import { ref } from 'vue'

const path = ref('')
const tableData = ref([])
const statusMsg = ref('')
const filterField = ref('')
const filterValue = ref('')

const API_URL = 'http://127.0.0.1:8000/api'

// Fonction générique pour appeler l'API
async function apiCall(endpoint, payload) {
  statusMsg.value = "Chargement..."
  try {
    const response = await fetch(`${API_URL}/${endpoint}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await response.json()
    
    if (data.status === 'error') throw new Error(data.message)
    
    statusMsg.value = "Succès !"
    return data
  } catch (e) {
    statusMsg.value = "Erreur : " + e.message
    return null
  }
}

async function loadData() {
  const res = await apiCall('load', { path: path.value })
  if (res) tableData.value = res.data
}

async function applyFilter() {
  const res = await apiCall('filter', { field: filterField.value, value: filterValue.value })
  if (res) tableData.value = res.data
}

async function sortCol(colName) {
  const res = await apiCall('sort', { field: colName })
  if (res) tableData.value = res.data
}
</script>

<template>
  <div class="viewer">
    <h2>Data Filter</h2>
    
    <div class="controls">
      <div class="group">
        <input v-model="path" placeholder="Chemin (ex: data/students.csv)" />
        <button @click="loadData">Charger Fichier</button>
      </div>
      
      <div class="group">
        <input v-model="filterField" placeholder="Champ (ex: age)" />
        <input v-model="filterValue" placeholder="Valeur (ex: 21)" />
        <button @click="applyFilter">Filtrer</button>
      </div>
    </div>

    <p class="status">{{ statusMsg }}</p>

    <div class="table-container" v-if="tableData.length">
      <table>
        <thead>
          <tr>
            <th v-for="(val, key) in tableData[0]" :key="key" @click="sortCol(key)">
              {{ key }} ↕
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in tableData" :key="i">
            <td v-for="(val, key) in row" :key="key">{{ val }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.viewer { max-width: 1000px; margin: 0 auto; }
.controls { display: flex; gap: 20px; margin-bottom: 20px; flex-wrap: wrap;}
.group { display: flex; gap: 10px; padding: 10px; background: #333; border-radius: 8px;}
input { padding: 8px; border-radius: 4px; border: 1px solid #555; background: #222; color: white;}
.table-container { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; margin-top: 10px; }
th, td { border: 1px solid #444; padding: 8px; text-align: left; }
th { background: #333; cursor: pointer; user-select: none;}
th:hover { background: #444; }
.status { color: #888; font-style: italic; }
</style>