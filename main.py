from cloudevents.http import CloudEvent
import functions_framework
from google.events.cloud import firestore as firestore_data
from google.cloud import firestore


db = firestore.Client()


@functions_framework.cloud_event
def create_data(cloud_event: CloudEvent) -> None:
    """Triggers by a change to a Firestore document.
    Args:
        cloud_event: cloud event with information on the firestore event trigger
    """
    firestore_payload = firestore_data.DocumentEventData()
    firestore_payload._pb.ParseFromString(cloud_event.data)

    print(f"Function triggered by change to: {cloud_event['source']}")
    url_path = firestore_payload.value.name
    print("url_path:::::::::::::::::::::::::::::::::::::::::::::", url_path)
    try:
        old_value = firestore_payload.old_value.fields["aadhar"].string_value
        new_value = firestore_payload.value.fields["aadhar"].string_value

        db.collection("update_data").add({
            "update_id": url_path.split("/d")[-1],
            "old_value": old_value,
            "new_value": new_value
        })

    except Exception as e:
        import traceback
        print("Traceback:", traceback.format_exc())
        print("Something went wrong :", str(e))
