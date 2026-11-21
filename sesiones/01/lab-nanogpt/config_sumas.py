# nanoGPT · lab sesión 1 · sumas. Pequeño a propósito: entrena en CPU en minutos.
out_dir = 'out-sumas'
dataset = 'sumas'
device = 'cpu'
compile = False
dtype = 'float32'
eval_interval = 250
eval_iters = 40
log_interval = 50
always_save_checkpoint = False
wandb_log = False

block_size = 64     # contexto: unas 7 sumas
batch_size = 32
gradient_accumulation_steps = 1  # nanoGPT trae 40 por defecto: en CPU eso es 40 veces más lento
n_layer = 4
n_head = 4
n_embd = 128
dropout = 0.0

learning_rate = 1e-3
max_iters = 3000
lr_decay_iters = 3000
min_lr = 1e-4
beta2 = 0.99
warmup_iters = 100
