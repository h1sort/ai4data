// ¿Cuántos tokens cuesta tu tabla? Tokenizadores de OpenAI (o200k_base y cl100k_base) vía gpt-tokenizer.
// Uso: npm install && node tokens.mjs [archivo.csv]
// Sin archivo: los ejemplos de la lámina más el CSV del caso.
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const ejemplos = ['7', '42', '999', '1000', '1234567', '3.14159', '1,234,567.89', '$1,249.50', '2026-11-21', '21/11/2026', 'CLI-0164', '23+45=68'];
const archivo = process.argv[2] ?? fileURLToPath(new URL('../../../caso/transacciones.csv', import.meta.url));
const lineas = fs.readFileSync(archivo, 'utf8').trim().split(/\r?\n/);

for (const nombre of ['o200k_base', 'cl100k_base']) {
  const t = await import(`gpt-tokenizer/encoding/${nombre}`);
  console.log(`\n== ${nombre}`);
  if (!process.argv[2]) for (const s of ejemplos) {
    const ids = t.encode(s);
    console.log(JSON.stringify(s).padEnd(16), String(ids.length).padStart(2), ids.map((i) => t.decode([i])).join(' | '));
  }
  const n = lineas.slice(1).map((l) => t.encode(l + '\n').length);
  const prom = n.reduce((a, b) => a + b, 0) / n.length;
  console.log(`\n${archivo}`);
  console.log(`  encabezado ${t.encode(lineas[0] + '\n').length} tokens · ${n.length} filas · ${prom.toFixed(1)} tokens por fila (min ${Math.min(...n)}, max ${Math.max(...n)})`);
  console.log(`  caben ~${Math.floor(200000 / prom).toLocaleString('es-MX')} filas en 200 mil tokens · ~${Math.floor(1e6 / prom).toLocaleString('es-MX')} en 1 millón`);
  const cols = lineas[0].split(','), por = cols.map(() => 0);
  for (const l of lineas.slice(1, 201)) l.split(',').forEach((v, i) => { if (i < cols.length) por[i] += t.encode(v).length; });
  const k = por.indexOf(Math.max(...por));
  console.log(`  columna más cara (primeras 200 filas): ${cols[k]}`);
}
