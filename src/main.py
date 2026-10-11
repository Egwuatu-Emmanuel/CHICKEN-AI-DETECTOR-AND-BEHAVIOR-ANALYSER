import cv2

from .config import (
    CONFIDENCE_THRESHOLD,
    WINDOW_NAME,
)

from .detector import ChickenDetector
from .tracker import ChickenTracker
from .behavior import BehaviorAnalyzer
from .camera import Camera
from .storage import Database
from .alerts import AlertManager


def get_center(box):

    x1, y1, x2, y2 = box

    center_x = int((x1 + x2) / 2)
    center_y = int((y1 + y2) / 2)

    return center_x, center_y


def main():

    print("Starting Poultry AI Monitor...")

    # -----------------------------------------------------
    # INITIALIZE COMPONENTS
    # -----------------------------------------------------

    detector = ChickenDetector()

    tracker = ChickenTracker(
        detector
    )

    behavior_analyzer = BehaviorAnalyzer()

    database = Database()

    alert_manager = AlertManager(
        stationary_threshold=10.0
    )

    camera = Camera("1,069 Chicken Farm House Videos, Clips and Stock Footage - Getty Images.mp4")

    print("System started.")
    print("Press Q to quit.")

    # -----------------------------------------------------
    # MAIN CAMERA LOOP
    # -----------------------------------------------------

    try:

        while True:

            frame = camera.read()

            # -------------------------------------------------
            # DETECTION + TRACKING
            # -------------------------------------------------

            results = tracker.track(
                frame,
                confidence=CONFIDENCE_THRESHOLD
            )

            result = results[0]

            # -------------------------------------------------
            # CHECK WHETHER TRACKING DATA EXISTS
            # -------------------------------------------------

            if result.boxes is not None:

                boxes = result.boxes

                # Tracking IDs may not exist yet
                if boxes.id is not None:

                    tracking_ids = boxes.id.cpu().numpy()

                    coordinates = boxes.xyxy.cpu().numpy()

                    confidences = boxes.conf.cpu().numpy()

                    classes = boxes.cls.cpu().numpy()

                    # -------------------------------------------------
                    # PROCESS EACH CHICKEN
                    # -------------------------------------------------

                    for box, track_id, confidence, class_id in zip(
                        coordinates,
                        tracking_ids,
                        confidences,
                        classes
                    ):

                        chicken_id = int(track_id)

                        class_id = int(class_id)

                        x1, y1, x2, y2 = map(
                            int,
                            box
                        )

                        center = get_center(
                            (x1, y1, x2, y2)
                        )

                        # ---------------------------------------------
                        # UPDATE BEHAVIOR
                        # ---------------------------------------------

                        chicken = (
                            behavior_analyzer.update_chicken(
                                chicken_id,
                                center
                            )
                        )

                        # ---------------------------------------------
                        # SAVE DATA
                        # ---------------------------------------------

                        database.save_activity(
                            chicken_id=chicken_id,
                            x=center[0],
                            y=center[1],
                            distance=chicken.total_distance,
                            speed=chicken.current_speed
                        )

                        # ---------------------------------------------
                        # CHECK ALERTS
                        # ---------------------------------------------

                        alert = (
                            alert_manager.check_chicken(
                                chicken
                            )
                        )

                        if alert:

                            print(
                                f"[ALERT] {alert}"
                            )

                        # ---------------------------------------------
                        # DRAW BOUNDING BOX
                        # ---------------------------------------------

                        cv2.rectangle(
                            frame,
                            (x1, y1),
                            (x2, y2),
                            (0, 255, 0),
                            2
                        )

                        # ---------------------------------------------
                        # DRAW CHICKEN ID
                        # ---------------------------------------------

                        label = (
                            f"Chicken #{chicken_id} "
                            f"{confidence:.2f}"
                        )

                        cv2.putText(
                            frame,
                            label,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 0),
                            2
                        )

                        # ---------------------------------------------
                        # DRAW CENTER POINT
                        # ---------------------------------------------

                        cv2.circle(
                            frame,
                            center,
                            5,
                            (255, 0, 0),
                            -1
                        )

                        # ---------------------------------------------
                        # DISPLAY MOVEMENT
                        # ---------------------------------------------

                        movement_text = (
                            f"Movement: "
                            f"{chicken.total_distance:.1f}px"
                        )

                        cv2.putText(
                            frame,
                            movement_text,
                            (x1, y2 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 255, 255),
                            1
                        )

            # -------------------------------------------------
            # DISPLAY CAMERA
            # -------------------------------------------------

            cv2.imshow(
                WINDOW_NAME,
                frame
            )

            # -------------------------------------------------
            # QUIT
            # -------------------------------------------------

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    finally:

        print("Shutting down...")

        camera.release()

        database.close()

        cv2.destroyAllWindows()

        print("System stopped.")


if __name__ == "__main__":
    main()