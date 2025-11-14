# %%
import pickle
import sys
import pandas as pd
from datetime import datetime
import argparse


# %%
def load_model(model_filename="Bank_train.pkl"):

    try:
        with open(model_filename, "rb") as f:
            package = pickle.load(f)
        print("The model was loaded from {}.".format(model_filename))
        return model_filename

    except FileNotFoundError:
        print("Error: The model file “{}” could not be found.".format(model_filename))
        sys.exit(1)
    except Exception as e:
        print("Error: Failed to load the model. -{}".format(e))
        sys.exit(1)


# %%
def create_features(df):
    x = df.copy()

    x["dur_hou"] = x["duration"] * x["housing_yes"]
    x["duration2"] = x["duration"] ** 2
    x["campaign2"] = x["campaign"] ** 2
    x["contact_sending _document3"] = x["contact_sending _document"] ** 3
    x["hou_cam_con"] = x["housing_yes"] * x["campaign"] * x["contact_sending _document"]
    x["dur_loa"] = x["duration"] * x["loan_yes"]
    x["loan_yes2"] = x["loan_yes"] ** 2
    x["age2"] = x["age"] ** 2
    x["hou_loa"] = x["housing_yes"] * x["loan_yes"]
    x["dur_cam"] = x["duration"] * x["campaign"]

    return x


# %%
def predict_csv(model, csv_path, output_path=None):
    try:
        df = pd.read_csv(csv_path)
        print("✓ The data has been loaded from “{}”.".format(csv_path))

        X = create_features(df)
        predictions = model.predict(X)
        probabilities = model.predict_proba(X)

        df["prediction"] = predictions
        df["prabability_class_0"] = probabilities[:, 0]
        df["prabability_class_1"] = probabilities[:, 1]
        df["prediction_label"] = df["prediction"].map({0: "Class 0", 1: "Class 1"})

        print("Predictive statistics:")
        print(
            f" Class 0: {(predictions == 0).sum()}items ({(predictions == 0).sum / len(predictions) * 100:.1f}%)"
        )
        print(
            f" Class 0: {(predictions == 1).sum()}items ({(predictions == 1).sum / len(predictions) * 100:.1f}%)"
        )

        if output_path is None:
            time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_output = "predictions_{}.csv".format(time_stamp)
            print("✓ Prediction results saved in '{}'!".format(default_output))
        else:
            df.to_csv(output_path, index=False, encoding="utf-8")
            print("✓ Prediction results saved in '{}'!".format(output_path))

    except FileNotFoundError:
        print("Error: The csv file “{}” could not be found.".format(csv_path))
        sys.exit(1)
    except Exception as e:
        print("Error: Failed to load the data. -{}".format(e))
        sys.exit(1)


# %%
def predict_interactive(model):
    print("Please enter the data to the following items.")

    try:
        id = int(input("id"))
        age = int(input("Age"))
        job = str(input("Job"))
        education = str(input("Final academic background"))
        marital = str(input("Marital"))
        loan = str(input("Presence of personal loan"))
        housing = str(input("Presence of mortgage loan"))
        amount = int(
            input(
                "Total investment trust purchase amount at the end of the annual campaign"
            )
        )
        default = str(input("Whether there is default"))
        previous = int(input("Number of contacts before the campaign"))
        campaign = int(input("Number of contacts within the current campaign"))
        day = int(input("Last contact date"))
        month = int(input("Last contact month"))
        duration = float(input("Average time of contact"))
        contact = str(input("Contact method"))

        input_data = pd.DataFrame(
            {
                "id": [id],
                "age": [age],
                "job": [job],
                "education": [education],
                "marital": [marital],
                "loan": [loan],
                "housing": [housing],
                "amount": [amount],
                "default": [default],
                "previous": [previous],
                "campaign": [campaign],
                "day": [day],
                "month": [month],
                "duration": [duration],
                "contact": [contact],
            }
        )

        X = create_features(input_data)

        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]

        print("Prediction result:")
        print(
            f"Whether to purchase or not: {'Purchased' if prediction == 1 else 'Not Purchased'}"
        )
        print(
            f"Probability of purchasing: {probabilities[1]:.4f} ({probabilities[1]*100:.2f}%)"
        )
        print(
            f"Probability of not purchasing: {probabilities[0]:.4f} ({probabilities[0]*100:.2f}%)"
        )
        print()

        if probabilities[1] > 0.8:
            print("Result: Very likely to purchase")
        elif probabilities[1] > 0.6:
            print("Result: Likely to purchase")
        elif probabilities[1] > 0.4:
            print("Result: It's a difficult case to decide")
        elif probabilities[1] > 0.2:
            print("Result: Unlikely to purchase")
        else:
            print("Result: Very unlikely to purchase")

    except ValueError as e:
        print(f"Error: Invalid input value - {e}")
    except KeyboardInterrupt:
        print("Prediction canceled")
    except Exception as e:
        print(f"Error: The prediction process failed - {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Use the trained model to make predictions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage example:
  # Interactive predictions
  python predict.py
  
  # Prediction from CSV file
  python predict.py --csv input.csv
  
  # Predict from a CSV file and save the results to a specified file
  python predict.py --csv input.csv --output results.csv
  
  # Use a different model file
  python predict.py --model my_model.pkl --csv input.csv
  """,
    )

    parser.add_argument("--csv", type=str, help="Input CSV file path")
    parser.add_argument(
        "--output", type=str, help="Path of the output CSV file (optional)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="model_complete_package.pkl",
        help="model file path（Default: model_complete_package.pkl）",
    )

    args = parser.parse_args()

    print()
    print("Prediction script")
    print()

    model_package = load_model(args.model)
    model = model_package["model"]

    if args.csv:
        predict_csv(model, args.csv, args.output)
    else:
        while True:
            predict_interactive(model)
            print()
            choice = input("Continue predicting? (y/n): ").lower()
            if choice != "y":
                print("\nPrediction ended.")
                break


if __name__ == "__main__":
    main()
