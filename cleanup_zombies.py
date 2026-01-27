
cr = env.cr
print("Starting cleanup for zombie models...")

models_to_clean = ['muon.tra', 'quan.ly.tai.san']

for model in models_to_clean:
    print(f"Cleaning up {model}...")
    
    # 1. Delete Selection fields
    cr.execute(f"DELETE FROM ir_model_fields_selection WHERE field_id IN (SELECT id FROM ir_model_fields WHERE model = '{model}')")
    print(f"  Deleted selection fields: {cr.rowcount}")

    # 2. Delete Fields
    cr.execute(f"DELETE FROM ir_model_fields WHERE model = '{model}'")
    print(f"  Deleted fields: {cr.rowcount}")

    # 3. Delete Access Rights
    cr.execute(f"DELETE FROM ir_model_access WHERE model_id IN (SELECT id FROM ir_model WHERE model = '{model}')")
    print(f"  Deleted access rights: {cr.rowcount}")

    # 4. Delete Constraints
    cr.execute(f"DELETE FROM ir_model_constraint WHERE model = (SELECT id FROM ir_model WHERE model = '{model}')")
    print(f"  Deleted constraints: {cr.rowcount}")

    # 5. Delete Relations
    cr.execute(f"DELETE FROM ir_model_relation WHERE model = (SELECT id FROM ir_model WHERE model = '{model}')")
    print(f"  Deleted relations: {cr.rowcount}")

    # 6. Delete XML Data
    cr.execute(f"DELETE FROM ir_model_data WHERE model = '{model}'")
    print(f"  Deleted data records: {cr.rowcount}")
    
    model_underscore = model.replace('.', '_')
    cr.execute(f"DELETE FROM ir_model_data WHERE name = 'model_{model_underscore}'")
    print(f"  Deleted model_{model_underscore} data ref: {cr.rowcount}")

    # 7. Delete the Model itself
    cr.execute(f"DELETE FROM ir_model WHERE model = '{model}'")
    print(f"  Deleted model: {cr.rowcount}")

cr.commit()
print("Cleanup complete.")
