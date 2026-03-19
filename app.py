from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# 🔷 HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')


# 🔷 AGENT PERFORMANCE (TUMHARA ORIGINAL DASHBOARD)
@app.route('/agent', methods=['GET', 'POST'])
def agent():
    if request.method == 'POST':
        agent_file = request.files['agent']
        cdr_file = request.files['cdr']

        df_agent = pd.read_excel(agent_file)
        df_cdr = pd.read_excel(cdr_file)

        df_agent.fillna(0, inplace=True)

        # 👉 SAME LOGIC (as your project)
        df_agent['Total Break'] = (
            df_agent['LUNCHBREAK'] +
            df_agent['TEABREAK'] +
            df_agent['SHORTBREAK']
        )

        df_agent['Net Login'] = (
            df_agent['Total Login Time'] - df_agent['Total Break']
        )

        # 🔥 IMPORTANT: YAHI CHANGE HAI
        # 👉 yaha apna ORIGINAL TEMPLATE NAME daalo
        return render_template('index.html',   # ⚠️ agar tumhara file naam alag hai to change karo
                               tables=df_agent.to_dict(orient='records'))

    return render_template('index.html')


# 🔷 FIRST LOGIN REPORT
@app.route('/firstlogin', methods=['GET', 'POST'])
def firstlogin():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_excel(file)

        df['Login Time'] = pd.to_datetime(df['Login Time'])

        first_login = (
            df.sort_values('Login Time')
              .groupby('Agent Name')
              .first()
              .reset_index()
        )

        return render_template('firstlogin.html',
                               tables=first_login.to_dict(orient='records'))

    return render_template('firstlogin.html')


if __name__ == "__main__":
    app.run(debug=True)
