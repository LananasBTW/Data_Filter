<script setup>
import { computed, onMounted, watch, ref, nextTick } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  report: { type: Object, required: true }
})

const emit = defineEmits(['close'])

const chartCanvas = ref(null)
let chartInstance = null

// Calcul des stats globales pour l'affichage HTML à droite
const globalStats = computed(() => {
  let ok = 0
  let nullCount = 0
  
  if (props.report) {
    Object.values(props.report).forEach(stats => {
      ok += stats.non_null_count
      nullCount += stats.null_count
    })
  }
  
  const total = ok + nullCount
  return { 
    ok, 
    nullCount, 
    total,
    okPercent: total ? Math.round((ok / total) * 100) : 0,
    nullPercent: total ? Math.round((nullCount / total) * 100) : 0
  }
})

function renderChart() {
  if (chartInstance) chartInstance.destroy()
  if (!chartCanvas.value) return

  chartInstance = new Chart(chartCanvas.value, {
    type: 'doughnut',
    data: {
      labels: ['Données Valides', 'Données Nulles'],
      datasets: [{
        data: [globalStats.value.ok, globalStats.value.nullCount],
        backgroundColor: ['#10b981', '#ef4444'],
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '75%', 
      plugins: {
        legend: { display: false }, 
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.label}: ${ctx.raw} (${Math.round(ctx.raw / globalStats.value.total * 100)}%)`
          }
        }
      }
    }
  })
}

watch(() => props.report, () => {
  nextTick(() => renderChart())
}, { deep: true })

onMounted(() => {
  renderChart()
})
</script>

<template>
  <div class="card stats-panel">
    <div class="card-header flex-between">
      <h3>Analyse & Graphique</h3>
      <button class="btn-icon" @click="$emit('close')">✕</button>
    </div>
    
    <div class="stats-content-wrapper">
      
      <div class="stats-top-section">
        <div class="chart-wrapper">
          <canvas ref="chartCanvas"></canvas>
        </div>

        <div class="stats-info-panel">
          <div class="total-block">
            <div class="big-number">{{ globalStats.total }}</div>
            <div class="big-label">Valeurs Analysées</div>
          </div>

          <ul class="stat-list">
            <li class="stat-item">
              <div class="stat-left">
                <span class="dot dot-green"></span>
                <span>Données Valides</span>
              </div>
              <div class="stat-right">
                {{ globalStats.ok }} 
                <span class="percent">({{ globalStats.okPercent }}%)</span>
              </div>
            </li>

            <li class="stat-item">
              <div class="stat-left">
                <span class="dot dot-red"></span>
                <span>Données Nulles</span>
              </div>
              <div class="stat-right">
                {{ globalStats.nullCount }} 
                <span class="percent">({{ globalStats.nullPercent }}%)</span>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div class="divider-full"></div>

      <div class="fields-grid-full">
        <div v-for="(stats, fieldName) in report" :key="fieldName" class="field-card">
            
            <div class="field-header">
                <span class="field-name">{{ fieldName }}</span>
                <div class="field-badges">
                    <span class="badge badge-success">{{ stats.non_null_count }} ok</span>
                    <span v-if="stats.null_count > 0" class="badge badge-danger">{{ stats.null_count }} null</span>
                </div>
            </div>

            <div class="types-container">
                <div v-for="(typeData, typeName) in stats.type_stats" :key="typeName" class="type-block">
                    <div class="type-label">{{ typeName }} <small>({{ typeData.count }})</small></div>

                    <div v-if="typeName === 'number'" class="stat-row">
                        <div class="mini-stat"><span>Min</span><strong>{{ typeData.min }}</strong></div>
                        <div class="mini-stat"><span>Moy</span><strong>{{ typeData.mean.toFixed(2) }}</strong></div>
                        <div class="mini-stat"><span>Max</span><strong>{{ typeData.max }}</strong></div>
                    </div>

                    <div v-else-if="typeName === 'bool'" class="stat-col">
                        <div class="progress-bar">
                            <div class="progress-fill true-fill" :style="{width: typeData.true_percentage + '%'}"></div>
                        </div>
                        <div class="bool-legend">
                            <span class="text-true">Vrai: {{ typeData.true_count }}</span>
                            <span class="text-false">Faux: {{ typeData.false_count }}</span>
                        </div>
                    </div>

                    <div v-else-if="typeName === 'str'" class="stat-col">
                        <div class="sample-list">
                            <span v-for="(sample, idx) in typeData.sample_values" :key="idx" class="sample-tag">
                                "{{ sample }}"
                            </span>
                        </div>
                    </div>

                    <div v-else-if="['list', 'dict'].includes(typeName)" class="stat-row">
                        <div class="mini-stat"><span>Min Len</span><strong>{{ typeData.size_min }}</strong></div>
                        <div class="mini-stat"><span>Moy Len</span><strong>{{ typeData.size_mean.toFixed(1) }}</strong></div>
                        <div class="mini-stat"><span>Max Len</span><strong>{{ typeData.size_max }}</strong></div>
                    </div>
                </div>
            </div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.stats-panel {
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 12px;
    margin-bottom: 20px;
    overflow: hidden;
}

.card-header {
    padding: 15px 20px;
    border-bottom: 1px solid #333;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #fff;
}

.card-header h3 {
    margin: 0;
    font-size: 1rem;
    color: #ccc;
    text-transform: uppercase;
}

.btn-icon {
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
    font-size: 1.2rem;
}

.btn-icon:hover { color: white; }

.stats-content-wrapper {
    padding: 30px;
    display: flex;
    flex-direction: column;
    gap: 30px;
}

/* --- TOP SECTION (LAYOUT) --- */
.stats-top-section {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 60px;
    padding-bottom: 10px;
}

.chart-wrapper {
    position: relative;
    height: 250px;
    width: 250px;
    flex-shrink: 0;
}

.stats-info-panel {
    display: flex;
    flex-direction: column;
    min-width: 220px;
}

.total-block {
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid #333;
}

.big-number {
    font-size: 2.5rem;
    font-weight: 800;
    color: white;
    line-height: 1;
}

.big-label {
    text-transform: uppercase;
    color: #888;
    font-size: 0.8rem;
    letter-spacing: 1px;
    margin-top: 5px;
}

.stat-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.stat-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.95rem;
}

.stat-left {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #ccc;
}

.dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.dot-green { background-color: #10b981; }
.dot-red { background-color: #ef4444; }

.stat-right {
    font-weight: bold;
    color: white;
}

.percent {
    font-weight: normal;
    color: #666;
    font-size: 0.85rem;
    margin-left: 5px;
}

.divider-full {
    height: 1px;
    background: #333;
    width: 100%;
}

/* --- BOTTOM SECTION (GRILLE) --- */
.fields-grid-full {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    width: 100%;
}

.field-card {
    background: #252525;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 15px;
    transition: transform 0.2s, box-shadow 0.2s;
    display: flex;
    flex-direction: column;
}

.field-card:hover {
    border-color: #555;
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

.field-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    border-bottom: 1px solid #3d3d3d;
    padding-bottom: 10px;
}

.field-name {
    font-weight: 700;
    color: #fff;
    font-size: 1rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 150px;
}

.field-badges {
    display: flex;
    gap: 5px;
    flex-shrink: 0;
}

.badge {
    font-size: 0.7rem;
    padding: 3px 6px;
    border-radius: 4px;
    font-weight: 600;
    text-transform: uppercase;
}

.badge-success { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); }
.badge-danger { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); }

.types-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex: 1; 
}

.type-block {
    background: rgba(0, 0, 0, 0.2);
    padding: 10px;
    border-radius: 8px;
    font-size: 0.9rem;
}

.type-label {
    color: #646cff;
    font-weight: 700;
    margin-bottom: 8px;
    display: block;
    text-transform: uppercase;
    font-size: 0.7rem;
    letter-spacing: 1px;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    background: rgba(255, 255, 255, 0.03);
    padding: 8px;
    border-radius: 6px;
}

.mini-stat {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
}

.mini-stat span { font-size: 0.65rem; color: #888; margin-bottom: 2px; }
.mini-stat strong { font-size: 0.9rem; color: #eee; font-weight: 600; }

.stat-col {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.progress-bar {
    height: 6px;
    background: #333;
    border-radius: 3px;
    overflow: hidden;
    width: 100%;
}

.progress-fill.true-fill {
    background: #10b981;
    height: 100%;
}

.bool-legend {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
}

.text-true { color: #10b981; }
.text-false { color: #ef4444; }

.sample-list {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}

.sample-tag {
    background: #333;
    padding: 3px 6px;
    border-radius: 4px;
    color: #ccc;
    font-family: monospace;
    font-size: 0.75rem;
    border: 1px solid #444;
}
</style>