import os
import datetime
from io import StringIO


class FR24Writer(object):
    """
    Main class for handling the data writing from FR24 .json files.

    Properties:
        flights (dict): Data points for each flight in csv format. This is done
                        by creating 'virtual' csv files with StringIO.
        timestamps (dict): First timestamp for each flight.
        callsigns (dict): Callsign for each flight.

        header, index (lists): Store the csv columns format.

        saveroot (str): Where to dump data to.
    """

    def __init__(self, saveroot):
        self.saveroot = saveroot

        self.flights = {}
        self.timestamps = {}
        self.callsigns = {}

        # Header for csv, and the corresponding index in the json data array
        self.header = ["time", "callsign", "latitude", "longitude", "altitude",
                       "ground_speed", "heading_angle"]
        self.index = [10, 16, 1, 2, 4, 5, 3]

    def set_saveroot(self, saveroot):
        """
        Reset the saveroot;
        useful for restoring a old FR24Writer and write data to somewhere else.
        """
        self.saveroot = saveroot

    def push(self, timestamp):
        """
        Push flight data to disk.

        First check if any flight has not received any new data point for more
        than 1 day (86400 seconds) from the passed timestamp.
        If so, then push data to disk and clean up.
        """

        pushed = []
        for k, t in self.timestamps.items():
            if (timestamp - t) >= 86400:
                self.push_flight(k)
                pushed.append(k)

        [self.clean_flight(k) for k in pushed]

    def push_safely(self):
        """
        Push all current flight data without time checking and cleaning up.
        """

        for k in self.flights:
            self.push_flight(k)

    def write(self, key, row):
        """
        Write a row from the FR24 json files to the corresponding flight csv.
        """

        # Create new flight first if this is the first point with this key
        if key not in self.flights:
            self.create(key, row[16], row[10])

        # Build the csv row to be written
        row_str = [str(row[i]) for i in self.index]
        row_csv = ",".join(row_str) + "\r\n"  # new line character

        self.flights[key].write(row_csv)

    def create(self, key, callsign, timestamp):
        """
        Create a new flight entry in the dictionaries.
        """

        self.flights[key] = StringIO()
        self.callsigns[key] = callsign
        self.timestamps[key] = timestamp

        # Write the header row
        row_header = ",".join(self.header) + "\r\n"  # new line character
        self.flights[key].write(row_header)

    def push_flight(self, key):
        """
        Store a particular flight to disk.
        """

        # Generate date string then create the date directory if not exist
        dt = datetime.datetime.utcfromtimestamp(self.timestamps[key])
        dirname = (f"{self.saveroot}/"
                   f"{dt.strftime('%Y-%m')}/{dt.strftime('%Y-%m-%d')}")

        if not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)

        # Dump the data from StringIO to file
        with open(f"{dirname}/{self.callsigns[key]}.csv", "w") as f:
            f.write(self.flights[key].getvalue())

    def clean_flight(self, key):
        """
        Delete all data for this flight to free up memory
        """
        self.flights[key].close()
        del self.flights[key]
        del self.timestamps[key]
        del self.callsigns[key]
