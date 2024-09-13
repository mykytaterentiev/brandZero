<template>
  <div class="overflow-x-auto h-full p-4">
    <h1 class="text-3xl font-bold mb-6 text-center">Transaction Data</h1>
    
    <ag-grid-vue
      class="ag-theme-alpine"
      style="width: 100%; height: 600px;"
      @grid-ready="onGridReady"
      :columnDefs="columnDefs"
      :defaultColDef="defaultColDef"
      :rowData="rowData"
      :pagination="true"
      :paginationPageSize="10"
    />
  </div>
</template>

<script setup lang="ts">
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { ref, onMounted } from 'vue';
import { AgGridVue } from 'ag-grid-vue3';
import axios from 'axios';

const columnDefs = ref([
  { field: 'id', headerName: 'ID', sortable: true, filter: 'agNumberColumnFilter' },
  { field: 'merchant_name', headerName: 'Merchant Name', sortable: true, filter: 'agTextColumnFilter' },
  { field: 'city', headerName: 'City', sortable: true, filter: 'agTextColumnFilter' },
  { field: 'mcc', headerName: 'MCC', sortable: true, filter: 'agNumberColumnFilter' },
  { field: 'country', headerName: 'Country', sortable: true, filter: 'agTextColumnFilter' },
  { field: 'embedding', headerName: 'Embedding (Preview)', sortable: false, filter: false, cellRenderer: (params: any) => params.value ? params.value.slice(0, 5) + '...' : '' },
]);

const defaultColDef = ref({
  flex: 1,
  minWidth: 150,
  resizable: true,
  filter: true,
});

const rowData = ref([]);

// Fetch data from the backend (transactions)
const fetchTransactions = async () => {
  try {
    const response = await axios.get('http://localhost:8000/transactions');
    console.log('API Response:', response.data);
    
    // Assuming response.data.transactions is an array of rows
    const transactions = response.data.transactions;
    console.log('Transactions Data:', transactions);

    rowData.value = transactions.map((tx: any) => ({
      id: tx[0],
      merchant_name: tx[1],
      city: tx[2],
      mcc: tx[3],
      country: tx[4],
      embedding: tx[5]
    }));
    
    console.log('Mapped Row Data:', rowData.value);
  } catch (error) {
    console.error('Error fetching transactions:', error);
  }
};

// Handle grid ready event
function onGridReady({ api }: { api: any }) {
  fetchTransactions();
}

onMounted(() => {
  fetchTransactions();
});
</script>

<style scoped>
.ag-theme-alpine {
  --ag-wrapper-border-radius: 8px;
  --ag-header-background-color: #f4f4f4;
  --ag-odd-row-background-color: #fff;
  --ag-alternate-row-background-color: #f9f9f9;
  --ag-header-foreground-color: #333;
  --ag-row-foreground-color: #333;
  --ag-cell-horizontal-border: 1px solid #ddd;
  --ag-header-cell-horizontal-border: 1px solid #ddd;
}

h1 {
  color: #1e3a8a;
}

.ag-theme-alpine .ag-root-wrapper {
  border: 0;
}

.ag-theme-alpine .ag-row {
  font-size: 14px;
}
</style>
