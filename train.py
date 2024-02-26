from transformers import GPT2Tokenizer, GPT2LMHeadModel
from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from transformers import TrainerCallback

dataset_path = "./datasets/All data_1.txt"
# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

train_dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=dataset_path,
    block_size=128,  # Adjust the block size according to your dataset
)

# Use the default data collator for language modeling
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False
)

# *    num_train_epochs=3,              # total number of training epochs*
# *    per_device_train_batch_size=16,  # batch size per device during training*
# *    per_device_eval_batch_size=16,   # batch size for evaluation*
# *    warmup_steps=50,                 # number of warmup steps for learning rate scheduler*
# *    weight_decay=0.01,               # strength of weight decay*
# *    logging_dir='./logs',            # directory for storing logs*
# *    logging_steps=20,*
# *    evaluation_strategy="steps"*        
# Define training arguments
training_args = TrainingArguments(
    output_dir="./anmialGPTV1",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=10_000,
    save_total_limit=2,
    logging_dir='./logs',            # directory for storing logs*
)

# Define a custom callback class to print steps and loss
class CustomCallback(TrainerCallback):
    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step % 100 == 0:
            print(f"Step {state.global_step}, Loss: {state.log_metrics['train_runtime'] / state.log_metrics['step']:.4f}")

# Create Trainer instance with the custom callback
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    callbacks=[CustomCallback()],
)

# Fine-tune the model
trainer.train()


# Save the fine-tuned model
model.save_pretrained("./anmialGPTV1")
tokenizer.save_pretrained("./anmialGPTV1")
