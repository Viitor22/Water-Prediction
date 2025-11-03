const form = document.getElementById('waterForm');
const statusSpan = document.getElementById('status');

function showError(msg) {
  statusSpan.innerHTML = `<span class="error">${msg}</span>`;
  setTimeout(() => { statusSpan.innerHTML = ''; }, 5000);
}

function validateRanges(data) {
  if (data.ph < 0 || data.ph > 14) return 'pH deve estar entre 0 e 14.';
  if (data.trihalomethanes > 1000) return 'Trihalometanos muito altos.';
  if (data.turbidity > 1000) return 'Turbidez parece inválida.';
  return '';
}

form.addEventListener('submit', async (ev) => {
  ev.preventDefault();
  statusSpan.innerHTML = 'Processando...';

  const fd = new FormData(form);
  const data = {
    ph: parseFloat(fd.get('ph')),
    hardness: parseFloat(fd.get('hardness')),
    solids: parseFloat(fd.get('solids')),
    chloramines: parseFloat(fd.get('chloramines')),
    sulfate: parseFloat(fd.get('sulfate')),
    conductivity: parseFloat(fd.get('conductivity')),
    organic_carbon: parseFloat(fd.get('organic_carbon')),
    trihalomethanes: parseFloat(fd.get('trihalomethanes')),
    turbidity: parseFloat(fd.get('turbidity')),
  };

  for (const [key, value] of Object.entries(data)) {
    if (value === '' || Number.isNaN(value)) {
      showError('Preencha todos os campos corretamente.');
      return;
    }
  }

  const rangeError = validateRanges(data);
  if (rangeError) {
    showError(rangeError);
    return;
  }

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      
      headers: {
        'Content-Type': 'application/json'
      },
      
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
      statusSpan.innerHTML = `<b>Resultado da Predição: ${result.prediction}</b>`;
    } else {
      showError(result.error);
    }

  } catch (error) {
    showError('Não foi possível conectar ao servidor. Tente novamente.');
  }
});