
cr = env.cr
print("Starting cleanup for phong.hop...")

# 1. Delete Selection fields related to phong.hop (children of ir_model_fields)
cr.execute("DELETE FROM ir_model_fields_selection WHERE field_id IN (SELECT id FROM ir_model_fields WHERE model = 'phong.hop')")
print(f"Deleted selection fields: {cr.rowcount}")

# 2. Delete Fields (children of ir_model)
cr.execute("DELETE FROM ir_model_fields WHERE model = 'phong.hop'")
print(f"Deleted fields: {cr.rowcount}")

# 3. Delete Access Rights (children of ir_model)
cr.execute("DELETE FROM ir_model_access WHERE model_id IN (SELECT id FROM ir_model WHERE model = 'phong.hop')")
print(f"Deleted access rights: {cr.rowcount}")

# 4. Delete Constraints (children of ir_model)
cr.execute("DELETE FROM ir_model_constraint WHERE model = (SELECT id FROM ir_model WHERE model = 'phong.hop')")
print(f"Deleted constraints: {cr.rowcount}")

# 5. Delete Relations (children of ir_model)
cr.execute("DELETE FROM ir_model_relation WHERE model = (SELECT id FROM ir_model WHERE model = 'phong.hop')")
print(f"Deleted relations: {cr.rowcount}")

# 6. Delete XML Data (ir_model_data) pointing to this model
cr.execute("DELETE FROM ir_model_data WHERE model = 'phong.hop'")
print(f"Deleted data records: {cr.rowcount}")
cr.execute("DELETE FROM ir_model_data WHERE name = 'model_phong_hop'")
print(f"Deleted model_phong_hop data ref: {cr.rowcount}")
cr.execute("DELETE FROM ir_model_data WHERE name LIKE '%phong_hop%' AND module = 'nhan_su'")
print(f"Deleted potential nhan_su refs: {cr.rowcount}")

# 7. Delete the Model itself
cr.execute("DELETE FROM ir_model WHERE model = 'phong.hop'")
print(f"Deleted model: {cr.rowcount}")

cr.commit()
print("Cleanup complete.")
