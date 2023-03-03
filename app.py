from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

conn = sql.connect("covid.db")
print("opened Database successfully")

conn.execute(""" CREATE TABLE IF NOT EXISTS covid
                (aadhar_num INT PRIMARY KEY NOT NULL,
                name VARCHAR(255) NOT NULL, 
                age INT NOT NULL,
                doses INT);""")

print("Table created successfully")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/enternew")
def new_person():
    return render_template("covid.html")

@app.route("/list", methods= ["POST", "GET"])
def view_details():
    return render_template("list.html")

@app.route("/addrec", methods= ["POST", "GET"])
def addrec():
    if request.method == "POST":
        try:
            aadhar = request.form["aadhar"]
            name = request.form["name"]
            age = request.form["age"]
            doses = request.form["doses"]

            with sql.connect("covid.db") as con:

                cur = con.cursor()
                cur.execute("INSERT INTO covid VALUES (?, ?, ?, ?)", (aadhar, name, age, doses))
                con.commit()
                msg = "Details added SUCCESSFULLY"

        except:
            con.rollback()
            msg = "Error in Inserting Operation"

        finally:
            con.close()
            return render_template("result.html", msg=msg)


@app.route("/data", methods= ["POST", "GET"])
def show_data():
    try:
            aadhar_no = request.form.get("aadhar_number")
            list1 = []
            list2 = []
            list3 = []
            list4 = []
            connection = sql.connect("covid.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * from covid WHERE aadhar_num = ?", (aadhar_no,))
            result1 = cursor.fetchall()
            # for i in result1:
            if len(result1) != 0:
                for i in result1:
                    list1.append(i[0])
                    list2.append(i[1])
                    list3.append(i[2])
                    list4.append(i[3])

            connection.commit()

    except:
        msg = "Record not found"

    finally:
        return render_template("data.html", count=len(list1), result1=list1, result2=list2, result3=list3, result4=list4)

if __name__ == "__main__":
    app.run(debug = True)