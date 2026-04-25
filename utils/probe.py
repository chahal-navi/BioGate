
output_dir = "extracted_tensors"

print("Loading Decoder (Sequence Intent) representations...")
X_train_dec = np.load(f"{output_dir}/X_train_decoder.npy")
y_train = np.load(f"{output_dir}/y_train.npy")

X_val_dec = np.load(f"{output_dir}/X_val_decoder.npy")
y_val = np.load(f"{output_dir}/y_val.npy")

# Combine them for rigorous K-Fold Cross Validation
X_all_dec = np.vstack([X_train_dec, X_val_dec])
y_all = np.concatenate([y_train, y_val])

print(f"Decoder Training Shape: {X_train_dec.shape[0]} proteins, {X_train_dec.shape[1]} features")


dec_probe = LogisticRegression(
    penalty='l1', 
    solver='liblinear', 
    C=0.5, 
    random_state=42
)

# 3. Stratified 5-Fold Cross Validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(dec_probe, X_all_dec, y_all, cv=cv, scoring='roc_auc')

print("\n" + "="*50)
print("       DECODER CROSS-VALIDATION REPORT")
print("="*50)
print(f"Fold ROC-AUC Scores: {np.round(cv_scores, 4)}")
print(f"True Average ROC-AUC: {np.mean(cv_scores):.4f} (+/- {np.std(cv_scores)*2:.4f})")

dec_probe.fit(X_train_dec, y_train)
surviving_dims = np.where(dec_probe.coef_[0] != 0)[0]
weights = dec_probe.coef_[0][surviving_dims]

print("\n--- Mechanistic Feature Survival ---")
print(f"Original Dimensions: 128")
print(f"Surviving Features after L1 penalty: {len(surviving_dims)}")

if len(surviving_dims) > 0:
    print("\nExact Surviving Dimensions:")
    for dim, weight in zip(surviving_dims, weights):
        print(f"  Dimension {dim:03d} | Coefficient: {weight:.4f}")
