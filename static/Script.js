// Script principal do formulário
const form = document.getElementById('waterForm');
const resultBox = document.getElementById('result');
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

form.addEventListener('submit', (ev) => {
  ev.preventDefault();
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
    potability: fd.get('potability') === '1' ? 'Potável' : 'Não potável'
  };

  // Verifica se todos os campos estão preenchidos
  for (const [k, v] of Object.entries(data)) {
    if (k !== 'potability' && (v === '' || Number.isNaN(v))) {
      showError('Preencha todos os campos corretamente.');
      return;
    }
  }

  const rangeError = validateRanges(data);
  if (rangeError) {
    showError(rangeError);
    return;
  }

  // Exibe o resultado
  resultBox.hidden = false;
  resultBox.innerHTML = `
    <strong>Valores:</strong>
    <ul>
      <li>pH da água: ${data.ph.toFixed(2)}</li>
      <li>Dureza: ${data.hardness} mg/L</li>
      <li>Sólidos totais dissolvidos: ${data.solids} ppm</li>
      <li>Cloraminas: ${data.chloramines} ppm</li>
      <li>Sulfato: ${data.sulfate} mg/L</li>
      <li>Condutividade: ${data.conductivity} µS/cm</li>
      <li>Carbono orgânico: ${data.organic_carbon} ppm</li>
      <li>Trihalometanos: ${data.trihalomethanes} µg/L</li>
      <li>Turbidez: ${data.turbidity} NTU</li>
    </ul>
  `;

  statusSpan.innerHTML = 'Dados validados com sucesso ✅';
  setTimeout(() => statusSpan.innerHTML = '', 4000);
});
