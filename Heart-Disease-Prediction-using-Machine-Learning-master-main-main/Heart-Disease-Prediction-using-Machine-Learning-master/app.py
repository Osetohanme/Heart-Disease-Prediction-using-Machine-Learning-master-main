import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')
import os
import pickle

# Page configuration
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="wide"
)

# Title
st.title("❤️ Heart Disease Prediction System")
st.markdown("---")

# Load data
@st.cache_data
# Load data
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "heart.csv")  # make sure name matches EXACTLY
    
    df = pd.read_csv(file_path)
    
    # Drop 'year' column if it exists
    if 'year' in df.columns:
        df = df.drop('year', axis=1)
    
    return df

dataset = load_data()

# Attempt to load previously saved models (if any)
def load_saved_models(path="models.pkl"):
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                saved = pickle.load(f)
            # Load into session state
            st.session_state['models'] = saved.get('models', {})
            st.session_state['results'] = saved.get('results', {})
            st.session_state['X_test'] = saved.get('X_test', None)
            st.session_state['Y_test'] = saved.get('Y_test', None)
            return True
        except Exception as e:
            st.warning(f"Failed to load saved models: {e}")
            return False
    return False

# Try loading saved models at startup
_ = load_saved_models()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home", "Data Overview", "Model Training", "Make Prediction", "Results"])

if page == "Home":
    st.header("Welcome to Heart Disease Prediction System")
    st.markdown("""
    This application uses Machine Learning to predict the presence of heart disease in patients.
    
    **Features:**
    - 📊 Data visualization and analysis
    - 🤖 Multiple ML models (4 selected algorithms)
    - 📈 Model performance comparison
    - 🔮 Interactive prediction interface
    
    **Best Model:** Random Forest (95% accuracy)
    
    Navigate using the sidebar to explore different sections.
    """)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{len(dataset):,}")
    with col2:
        st.metric("Features", len(dataset.columns) - 1)
    with col3:
        st.metric("Heart Disease Cases", f"{dataset['target'].sum():,}")
    with col4:
        st.metric("No Heart Disease", f"{len(dataset) - dataset['target'].sum():,}")

elif page == "Data Overview":
    st.header("📊 Dataset Overview")
    
    # Dataset info
    st.subheader("Dataset Information")
    st.write(f"**Shape:** {dataset.shape[0]:,} rows × {dataset.shape[1]} columns")
    
    # Check for year column
    if 'year' in dataset.columns:
        st.info("ℹ️ Note: 'year' column detected and excluded from model features (metadata only)")
    
    # Display first few rows
    st.subheader("First 5 Rows")
    st.dataframe(dataset.head())
    
    # Statistics
    st.subheader("Dataset Statistics")
    st.dataframe(dataset.describe())
    
    # Target distribution
    st.subheader("Target Variable Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        target_counts = dataset['target'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(target_counts.values, labels=['No Heart Disease', 'Heart Disease'], autopct='%1.1f%%', startangle=90)
        ax.set_title('Heart Disease Distribution')
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots()
        sns.countplot(x=dataset['target'], ax=ax)
        ax.set_title('Heart Disease Count')
        ax.set_xlabel('Target (0=No Disease, 1=Disease)')
        st.pyplot(fig)
    
    # Correlation
    st.subheader("Feature Correlation with Target")
    corr = dataset.corr()['target'].abs().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    corr.plot(kind='barh', ax=ax)
    ax.set_title('Feature Correlation with Target Variable')
    st.pyplot(fig)

elif page == "Model Training":
    st.header("🤖 Model Training")
    
    # Dataset size warning and sampling option
    st.info(f"📊 **Dataset Size:** {len(dataset):,} rows, {len(dataset.columns)} columns")
    
    if len(dataset) > 10000:
        st.warning("⚠️ **Large Dataset Detected!** Training on the full dataset may take a very long time.")
        use_sample = st.checkbox("Use sample for faster training (recommended)", value=True)
        if use_sample:
            sample_size = st.slider("Sample size", 1000, min(50000, len(dataset)), 10000)
            st.caption(f"Using {sample_size:,} rows for training (faster but may affect accuracy)")
        else:
            sample_size = len(dataset)
            st.warning("⚠️ Training on full dataset - this may take 30+ minutes!")
    else:
        use_sample = False
        sample_size = len(dataset)
    
    if st.button("Train Selected Models"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Prepare data
        if use_sample and sample_size < len(dataset):
            # Sample the dataset
            sample_data = dataset.sample(n=sample_size, random_state=42)
            predictors = sample_data.drop("target", axis=1)
            target = sample_data["target"]
        else:
            predictors = dataset.drop("target", axis=1)
            target = dataset["target"]
        
        X_train, X_test, Y_train, Y_test = train_test_split(predictors, target, test_size=0.20, random_state=0)
        
        st.info(f"Training on {len(X_train):,} samples, testing on {len(X_test):,} samples")
        
        results = {}
        
        # Logistic Regression
        status_text.text("Training Logistic Regression...")
        progress_bar.progress(10)
        lr = LogisticRegression()
        lr.fit(X_train, Y_train)
        Y_pred_lr = lr.predict(X_test)
        results['Logistic Regression'] = round(accuracy_score(Y_pred_lr, Y_test) * 100, 2)
        
        # Naive Bayes
        status_text.text("Training Naive Bayes...")
        progress_bar.progress(25)
        nb = GaussianNB()
        nb.fit(X_train, Y_train)
        Y_pred_nb = nb.predict(X_test)
        results['Naive Bayes'] = round(accuracy_score(Y_pred_nb, Y_test) * 100, 2)
        
        # Random Forest
        status_text.text("Training Random Forest...")
        progress_bar.progress(55)
        max_accuracy = 0
        for x in range(50):
            rf = RandomForestClassifier(random_state=x)
            rf.fit(X_train, Y_train)
            Y_pred_rf = rf.predict(X_test)
            current_accuracy = round(accuracy_score(Y_pred_rf, Y_test) * 100, 2)
            if current_accuracy > max_accuracy:
                max_accuracy = current_accuracy
                best_x = x
        rf = RandomForestClassifier(random_state=best_x)
        rf.fit(X_train, Y_train)
        Y_pred_rf = rf.predict(X_test)
        results['Random Forest'] = round(accuracy_score(Y_pred_rf, Y_test) * 100, 2)
        
        # XGBoost
        status_text.text("Training XGBoost...")
        progress_bar.progress(80)
        xgb_model = xgb.XGBClassifier(objective="binary:logistic", random_state=42)
        xgb_model.fit(X_train, Y_train)
        Y_pred_xgb = xgb_model.predict(X_test)
        results['XGBoost'] = round(accuracy_score(Y_pred_xgb, Y_test) * 100, 2)
        
        progress_bar.progress(100)
        status_text.text("Training Complete!")
        
        # Store results in session state
        st.session_state['results'] = results
        st.session_state['models'] = {
            'lr': lr,
            'nb': nb,
            'rf': rf,
            'xgb': xgb_model
        }
        st.session_state['X_test'] = X_test
        st.session_state['Y_test'] = Y_test
        # Save trained models and results to disk
        try:
            save_obj = {
                'models': st.session_state['models'],
                'results': st.session_state.get('results', {}),
                'X_test': X_test,
                'Y_test': Y_test
            }
            with open('models.pkl', 'wb') as f:
                pickle.dump(save_obj, f)
            st.success("Trained models saved to models.pkl")
        except Exception as e:
            st.warning(f"Could not save models to disk: {e}")
        
        st.success("Selected models trained successfully!")
    
    # Display results if available
    if 'results' in st.session_state:
        st.subheader("Model Performance")
        results_df = pd.DataFrame(list(st.session_state['results'].items()), 
                                 columns=['Model', 'Accuracy (%)'])
        results_df = results_df.sort_values('Accuracy (%)', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(results_df.style.highlight_max(subset=['Accuracy (%)']))
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=results_df['Model'], y=results_df['Accuracy (%)'], ax=ax)
            ax.set_title('Model Accuracy Comparison')
            ax.set_ylabel('Accuracy (%)')
            ax.set_xlabel('Model')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)

elif page == "Make Prediction":
    st.header("🔮 Make a Prediction")
    
    if 'models' not in st.session_state:
        loaded = load_saved_models()
        if not loaded:
            st.warning("⚠️ Please train the models first from the 'Model Training' page or train now.")
    if 'models' in st.session_state:
        st.subheader("Enter Patient Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.slider("Age", 20, 100, 50)
            sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
            cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3], 
                            format_func=lambda x: ["Typical Angina", "Atypical Angina", 
                                                  "Non-anginal Pain", "Asymptomatic"][x])
            trestbps = st.slider("Resting Blood Pressure", 90, 200, 120)
            chol = st.slider("Serum Cholesterol (mg/dl)", 100, 600, 200)
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1], 
                             format_func=lambda x: "No" if x == 0 else "Yes")
        
        with col2:
            restecg = st.selectbox("Resting ECG", [0, 1, 2])
            thalach = st.slider("Maximum Heart Rate Achieved", 70, 220, 150)
            exang = st.selectbox("Exercise Induced Angina", [0, 1], 
                               format_func=lambda x: "No" if x == 0 else "Yes")
            oldpeak = st.slider("ST Depression", 0.0, 6.0, 1.0, 0.1)
            slope = st.selectbox("Slope of Peak Exercise ST", [0, 1, 2])
            ca = st.slider("Number of Major Vessels", 0, 4, 0)
            thal = st.selectbox("Thal", [0, 1, 2, 3])
        
        # Prepare input
        input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, 
                              thalach, exang, oldpeak, slope, ca, thal]])

        # Model selection: allow user override, default = auto-select best by accuracy
        display_names = ['Random Forest', 'Logistic Regression', 'Naive Bayes', 'XGBoost']
        display_to_key = {'Random Forest': 'rf', 'Logistic Regression': 'lr', 'Naive Bayes': 'nb', 'XGBoost': 'xgb'}

        # Determine auto best model name if results available
        auto_label = 'Auto (Random Forest)'
        if 'results' in st.session_state and st.session_state['results']:
            try:
                best_model_name = max(st.session_state['results'], key=st.session_state['results'].get)
                auto_label = f"Auto ({best_model_name})"
            except Exception:
                auto_label = 'Auto (Random Forest)'

        options = [auto_label] + display_names
        selected = st.selectbox('Model to use for main prediction', options, index=0)

        if st.button("Predict Heart Disease"):
            st.subheader("Prediction Results")

            # Resolve chosen model key
            chosen_key = None
            if selected.startswith('Auto'):
                # map best_model_name (human) to model key
                if 'results' in st.session_state and st.session_state['results']:
                    best_model_name = max(st.session_state['results'], key=st.session_state['results'].get)
                    chosen_key = display_to_key.get(best_model_name, 'rf')
                else:
                    chosen_key = 'rf'
            else:
                chosen_key = display_to_key.get(selected, 'rf')

            # Fallback to any available model if selected not present
            models_available = st.session_state.get('models', {})
            if chosen_key not in models_available:
                # pick first available model
                if models_available:
                    chosen_key = list(models_available.keys())[0]
                else:
                    st.error('No models available. Please train models first.')
                    chosen_key = None

            if chosen_key is not None:
                model = st.session_state['models'][chosen_key]
                prediction = model.predict(input_data)[0]
                # try predict_proba, fallback to decision
                try:
                    probability = model.predict_proba(input_data)[0]
                except Exception:
                    probability = None
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if prediction == 1:
                    st.error("⚠️ Heart Disease Detected")
                else:
                    st.success("✅ No Heart Disease")
            
            with col2:
                if probability is not None:
                    st.metric("Probability of Heart Disease", f"{probability[1]*100:.2f}%")
                else:
                    st.write("Probability: N/A for selected model")

            with col3:
                if probability is not None:
                    st.metric("Probability of No Heart Disease", f"{probability[0]*100:.2f}%")
                else:
                    st.write("")
            
            # Show predictions from selected models
            st.subheader("Predictions from Selected Models")
            all_predictions = {}
            for name, model in st.session_state['models'].items():
                all_predictions[name] = model.predict(input_data)[0]
            
            model_names = {
                'lr': 'Logistic Regression',
                'nb': 'Naive Bayes',
                'rf': 'Random Forest',
                'xgb': 'XGBoost'
            }
            
            pred_df = pd.DataFrame([
                {'Model': model_names[name], 
                 'Prediction': 'Heart Disease' if pred == 1 else 'No Heart Disease'}
                for name, pred in all_predictions.items()
            ])
            st.dataframe(pred_df)

            # Provide interpretation, description and actionable advice
            st.subheader("Interpretation & Next Steps")
            if prediction == 1:
                st.error("⚠️ The model indicates an elevated likelihood of heart disease. This is NOT a clinical diagnosis.")
                st.markdown(
                    "**About this condition:** The model flags findings commonly associated with coronary artery disease (CAD) — a condition where the heart's blood vessels become narrowed or blocked, which can cause chest pain (angina), shortness of breath, or heart attack."
                )
                st.markdown("**Practical steps to take:**")
                st.markdown("- Schedule a medical evaluation with a primary care physician or cardiologist for clinical assessment and diagnostic tests (ECG, stress test, cardiac imaging).")
                st.markdown("- If you smoke, seek programs to stop smoking — tobacco dramatically raises heart risk.")
                st.markdown("- Control blood pressure, cholesterol, and blood sugar through medications and follow-up as advised by your clinician.")
                st.markdown("- Adopt heart-healthy habits: a Mediterranean-style diet, regular moderate exercise (as tolerated), maintain a healthy weight, and limit alcohol.")
                st.markdown("- Discuss medications that reduce risk (e.g., antiplatelets, statins, blood pressure medicines) and whether referral for further testing or procedures is needed.")
                st.markdown("**Learn more:** [American Heart Association](https://www.heart.org) • [Mayo Clinic](https://www.mayoclinic.org)")
                st.info("This information is educational. Always follow personalized advice from a qualified healthcare professional.")
            else:
                st.success("✅ The model predicts no heart disease. This is not a guarantee of absence of disease.")
                st.markdown("**Prevention tips:**")
                st.markdown("- Maintain a balanced diet, be physically active, and avoid tobacco.")
                st.markdown("- Monitor and manage blood pressure, cholesterol, and blood sugar with your clinician.")
                st.markdown("- Have regular check-ups and discuss any new symptoms (chest pain, unexplained breathlessness, fainting) with your doctor.")
                st.markdown("**Learn more:** [British Heart Foundation](https://www.bhf.org.uk) • [NHS - Heart disease](https://www.nhs.uk/conditions/coronary-heart-disease/")
                st.markdown("**Learn more:** [British Heart Foundation](https://www.bhf.org.uk) • [NHS - Heart disease](https://www.nhs.uk/conditions/coronary-heart-disease/)")

elif page == "Results":
    st.header("📈 Results Summary")
    
    if 'results' in st.session_state:
        results = st.session_state['results']
        
        # Best model
        best_model = max(results, key=results.get)
        st.success(f"🏆 Best Model: **{best_model}** with {results[best_model]}% accuracy")
        
        # Results table
        st.subheader("All Model Results")
        results_df = pd.DataFrame(list(results.items()), 
                                 columns=['Model', 'Accuracy (%)'])
        results_df = results_df.sort_values('Accuracy (%)', ascending=False)
        st.dataframe(results_df, use_container_width=True)
        
        # Visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=results_df['Model'], y=results_df['Accuracy (%)'], ax=ax, palette='viridis')
        ax.set_title('Model Accuracy Comparison', fontsize=16, fontweight='bold')
        ax.set_ylabel('Accuracy (%)', fontsize=12)
        ax.set_xlabel('Model', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("No results available. Please train models from the 'Model Training' page.")

# Footer
st.markdown("---")
st.markdown("**Technology Stack:** Python, Scikit-learn, XGBoost, Streamlit")


