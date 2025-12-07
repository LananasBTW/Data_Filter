<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: { type: Array, default: () => [] },
  currentPage: Number,
  totalPages: Number
})

const emit = defineEmits(['sort', 'page-change'])

const headers = computed(() => {
  if (props.data && props.data.length > 0) {
    return Object.keys(props.data[0])
  }
  return []
})

function isObject(val) {
  return typeof val === 'object' && val !== null
}
</script>

<template>
  <div class="card table-card">
    <div v-if="data.length" class="table-responsive">
      <table>
        <thead>
          <tr>
            <th v-for="key in headers" :key="key" @click="$emit('sort', key)">
              <div class="th-content">{{ key }} <span class="sort-arrow">↕</span></div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in data" :key="i">
            <td v-for="(val, key) in row" :key="key">
              <span class="cell-content">
                {{ isObject(val) ? JSON.stringify(val) : val }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-else class="empty-state">
      <div class="empty-icon">Data</div>
      <p>Aucune donnée chargée.</p>
    </div>

    <div v-if="data.length > 0" class="pagination-footer">
      <span class="page-info">Page {{ currentPage }} / {{ totalPages }}</span>
      <div class="page-controls">
        <button @click="$emit('page-change', -1)" :disabled="currentPage === 1" class="btn-sm btn-secondary">Précédent</button>
        <button @click="$emit('page-change', 1)" :disabled="currentPage === totalPages" class="btn-sm btn-secondary">Suivant</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.table-card {
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    min-height: 400px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
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
    z-index: 10;
    cursor: pointer;
    user-select: none;
}

th:hover {
    color: white;
    background: #222;
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

.sort-arrow { opacity: 0.3; }
th:hover .sort-arrow { opacity: 1; }

.pagination-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-top: 1px solid #333;
    background: #1a1a1a;
}

.page-info { font-size: 0.85rem; color: #aaa; }
.page-controls { display: flex; gap: 10px; }

.btn-sm {
    padding: 5px 12px;
    font-size: 0.8rem;
    border-radius: 4px;
    cursor: pointer;
    border: 1px solid #444;
    background: #333;
    color: white;
}
.btn-sm:disabled { opacity: 0.5; cursor: not-allowed; }

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
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 10px;
    opacity: 0.2;
}
</style>