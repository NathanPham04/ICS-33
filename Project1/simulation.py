from pathlib import Path
from collections import namedtuple

Message = namedtuple('Message', ['type', 'sender', 'description', 'time', 'sent', 'receiver'])
Propagation = namedtuple('Propagation', ['destination', 'time'])

class Simulation:
    def __init__(self, file_path: Path):
        # Initializes the simulation with the input path, a dict for devices, list for rules, a
        # simulation time of 0 for the beginning, and a list of messages
        self.file = file_path
        self.devices = dict()
        self.rules = []
        self.length = 0
        self.messages = []

    def read_file(self) -> None:
        # Reads the input file and puts devices into device list and determines the time length
        try:
            with open(self.file) as temp_file:
                for line in temp_file:
                    self._read_line(line)
        except:
            print('FILE NOT FOUND')
            quit()
    # One of the lines is just hit by coverage because its if statement is always true and the else
    # is never tested
    def _read_line(self, line: str) -> None:
        # Will take in a line of text and process it accordingly to what it will mean in the simulation
        line_elements = line.split()
        if len(line_elements) == 0 or line_elements[0][0] == '#':
            return
        else:
            if line_elements[0] == 'LENGTH':
                self.length = int(line_elements[1]) * 60 * 1000
            elif line_elements[0] == 'DEVICE':
                self.devices[line_elements[1]] = Device(int(line_elements[1]), self)
            elif line_elements[0] == 'PROPAGATE':
                self.rules.append((int(line_elements[1]), int(line_elements[2]), int(line_elements[3])))
            elif line_elements[0] == 'ALERT' or line_elements[0] == 'CANCEL':
                self.messages.append(Message(line_elements[0], int(line_elements[1]), line_elements[2], int(line_elements[3]), True, None))
    def set_device_rules(self) -> None:
        # Will loop through all the rules and set it for each device
        for rule in self.rules:
            device, destination, time = rule
            self.devices[str(device)].add_rule(Propagation(destination, time))

    def sort_messages(self) -> None:
        # Sorts the all the messages in self.messages by time
        self.messages = sorted(self.messages, key=lambda message: message.time)

    def start_simulation(self) -> None:
        # This will start the simulation and run till the end
        self.messages.append(Message('END', None, None, self.length, None, None))
        while self.messages[0].time < self.length:
            current = self.get_current_messages()
            self.sort_current_messages(current)
            self.sort_messages()
        print(f'@{self.length}: END')
    def sort_current_messages(self, current: list['Message']) -> None:
        # This will sort the current messages into the proper order and propagate them
        id_sorted = self.sort_by_id(current)
        to_initiate = []
        while len(id_sorted) != 0:
            current_device_messages = self.get_single_id(id_sorted)
            to_initiate.extend(self.process_current_messages_device(current_device_messages))
        self.initiate_messages(to_initiate)

    def process_current_messages_device(self, current: list['Message']) -> list['Message']:
        # This will process all the current messages of a device
        to_receive = []
        to_send = []
        for message in current:
            if message.sent:
                to_send.append(message)
            else:
                to_receive.append(message)
        to_cancel, to_alert = self.sort_cancel_and_alert(to_receive)
        for message in to_cancel:
            device = self.devices[str(message.receiver)]
            device.receive(message)
        for message in to_alert:
            device = self.devices[str(message.receiver)]
            device.receive(message)
        return to_send
    def initiate_messages(self, to_send: list['Message']) -> None:
        # This will process all the messages that are set to be initiated
        if len(to_send) != 0:
            to_cancel, to_alert = self.sort_cancel_and_alert(to_send)
            for message in to_cancel:
                device = self.devices[str(message.sender)]
                if message.description in device.cancellations:
                    pass
                else:
                    device.cancellations.add(message.description)
                    device.send(message)
            for message in to_alert:
                device = self.devices[str(message.sender)]
                if message.description in device.cancellations:
                    pass
                else:
                    device.send(message)
    @staticmethod
    def sort_cancel_and_alert(message_list: list['Message']) -> tuple[list['Message'], list['Message']]:
        # This will take in a list and sort them by cancels and alerts and then by sender and description
        to_cancel = [message for message in message_list if message.type == 'CANCEL']
        to_alert = [message for message in message_list if message.type == 'ALERT']
        to_cancel.sort(key = lambda x: (x.sender, x.description))
        to_alert.sort(key = lambda x: (x.sender, x.description))
        return to_cancel, to_alert
    @staticmethod
    def sort_by_id(current: list['Message']) -> list['Message']:
        # This will sort the current messages by device id
        to_receive = [x for x in current if not x.receiver is None]
        to_send = [x for x in current if x.receiver is None]
        to_receive.sort(key=lambda x: x.receiver)
        to_receive.extend(to_send)
        return to_receive
    @staticmethod
    def get_single_id(current: list['Message']) -> list['Message']:
        # This will get the messages of a single device id out first
        current_device_messages = [current.pop(0)]
        while len(current) != 0:
            if current[0].sender == current_device_messages[0].sender:
                current_device_messages.append(current.pop(0))
            else:
                break
        return current_device_messages

    def get_current_messages(self) -> list['Message']:
        # This will get the messages that will occur first and propagate them
        current_messages = [self.messages.pop(0)]
        time = current_messages[0].time
        while True:
            if self.messages[0].time == time:
                current_messages.append(self.messages.pop(0))
            else:
                return current_messages
class Device:
    def __init__(self, device_id: int, simulation: Simulation) -> None:
        # Initializes the device with an id and an empty rules list
        self._device_id = device_id
        self.rules = []
        self.cancellations = set()
        self.sim = simulation

    def get_id(self) -> int:
        # Returns the id of device
        return self._device_id

    def get_rules(self) -> list:
        # Returns the propagation rules of the device
        return self.rules

    def add_rule(self, rule: Propagation) -> None:
        # Adds a propagation rule to the rules list
        self.rules.append(rule)
    def receive(self, message: Message) -> None:
        # Receives a message
        to_print = message.type
        if message.type == 'CANCEL':
            to_print = 'CANCELLATION'
        print(f'@{message.time}: #{self.get_id()} RECEIVED {to_print} FROM #{message.sender}: {message.description}')
        if message.type == 'ALERT':
            if message.description in self.cancellations:
                pass
            else:
                self.send(message)
        else:
            if message.description in self.cancellations:
                pass
            else:
                self.cancellations.add(message.description)
                self.send(message)
    def send(self, message: Message) -> None:
        # Sends a message
        to_print = message.type
        if message.type == 'CANCEL':
            to_print = 'CANCELLATION'
        self.rules.sort(key=lambda x: x.destination)
        for rule in self.rules:
            new_receiver = rule.destination
            new_time = message.time + rule.time
            new_message = message._replace(sender=self.get_id(), time=new_time, sent=False, receiver=new_receiver)
            self.sim.messages.insert(0,new_message)
            print(f'@{message.time}: #{self.get_id()} SENT {to_print} TO #{new_receiver}: {message.description}')
