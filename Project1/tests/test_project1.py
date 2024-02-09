import unittest
from unittest.mock import patch
import project1
from simulation import *
import contextlib
import io
import tempfile


class TestProject1(unittest.TestCase):
    def setUp(self) -> None:
        self.sim = Simulation(Path('temp'))

    file_path = 'temp'
    @patch('builtins.input', return_value = file_path)
    def test_read_input_file_path(self, mock_input):
        ans = project1._read_input_file_path()
        self.assertEqual(ans, Path('temp'))

    @patch('builtins.input', return_value = file_path)
    def test_file_not_found(self, mock_input):
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                project1.main()
        self.assertEqual('FILE NOT FOUND\n', output.getvalue())

    def test_simulation_class_instantiation(self):
        self.assertEqual(Path('temp'), self.sim.file)
        self.assertEqual(dict(), self.sim.devices)
        self.assertEqual([], self.sim.rules)
        self.assertEqual(0, self.sim.length)
        self.assertEqual([], self.sim.messages)

    def test_read_line_empty(self):
        self.sim._read_line('')
        self.assertEqual(Path('temp'), self.sim.file)
        self.assertEqual(dict(), self.sim.devices)
        self.assertEqual([], self.sim.rules)
        self.assertEqual(0, self.sim.length)
        self.assertEqual([], self.sim.messages)

    def test_read_line_spaces(self):
        self.sim._read_line('            ')
        self.assertEqual(Path('temp'), self.sim.file)
        self.assertEqual(dict(), self.sim.devices)
        self.assertEqual([], self.sim.rules)
        self.assertEqual(0, self.sim.length)
        self.assertEqual([], self.sim.messages)

    def test_read_line_comments(self):
        self.sim._read_line('#        ')
        self.assertEqual(Path('temp'), self.sim.file)
        self.assertEqual(dict(), self.sim.devices)
        self.assertEqual([], self.sim.rules)
        self.assertEqual(0, self.sim.length)
        self.assertEqual([], self.sim.messages)

    def test_read_line_length(self):
        self.sim._read_line('LENGTH 2')
        self.assertEqual(120_000, self.sim.length)

    def test_read_line_device(self):
        self.sim._read_line('DEVICE 2')
        self.assertEqual(type(Device(2, self.sim)), type(self.sim.devices['2']))
        self.assertEqual(2, self.sim.devices['2'].get_id())

    def test_read_line_propagate(self):
        self.sim._read_line('PROPAGATE 1 2 100')
        self.assertEqual((1,2,100),self.sim.rules[0])

    def test_read_line_alert(self):
        self.sim._read_line('ALERT 1 OhNo 5000')
        self.assertEqual(Message, type(self.sim.messages[0]))
        self.assertEqual('ALERT', self.sim.messages[0].type)
        self.assertEqual(1, self.sim.messages[0].sender)
        self.assertEqual('OhNo', self.sim.messages[0].description)
        self.assertEqual(5000, self.sim.messages[0].time)

    def test_read_line_cancellation(self):
        self.sim._read_line('CANCEL 1 OhNo 5000')
        self.assertEqual(Message, type(self.sim.messages[0]))
        self.assertEqual('CANCEL', self.sim.messages[0].type)
        self.assertEqual(1, self.sim.messages[0].sender)
        self.assertEqual('OhNo', self.sim.messages[0].description)
        self.assertEqual(5000, self.sim.messages[0].time)

    def test_setting_device_rules(self):
        self.sim._read_line('PROPAGATE 1 2 100')
        self.sim._read_line('DEVICE 1')
        self.sim._read_line('DEVICE 2')
        self.sim.set_device_rules()
        self.assertEqual(2, self.sim.devices['1'].get_rules()[0].destination)
        self.assertEqual(100, self.sim.devices['1'].get_rules()[0].time)

    def test_setting_device_rules_multiple(self):
        self.sim._read_line('PROPAGATE 1 2 100')
        self.sim._read_line('PROPAGATE 1 3 1000')
        self.sim._read_line('DEVICE 1')
        self.sim._read_line('DEVICE 2')
        self.sim._read_line('DEVICE 3')
        self.sim.set_device_rules()
        self.assertEqual(3, self.sim.devices['1'].get_rules()[1].destination)
        self.assertEqual(1000, self.sim.devices['1'].get_rules()[1].time)

    def test_sort_messages(self):
        self.sim._read_line('CANCEL 1 3 2000')
        self.sim._read_line('ALERT 1 2 100')
        self.sim._read_line('CANCEL 1 2 200')
        self.sim._read_line('ALERT 1 3 1000')
        self.sim._read_line('CANCEL 8 3 2100')
        self.sim._read_line('ALERT 3 2 101')
        self.sim._read_line('CANCEL 6 2 230')
        self.sim.sort_messages()
        l = [x.time for x in self.sim.messages]
        self.assertEqual([100, 101, 200, 230, 1000, 2000, 2100], l)

    def test_begin_get_current_messages(self):
        self.sim._read_line('CANCEL 1 3 20')
        self.sim._read_line('ALERT 1 2 20')
        self.sim._read_line('CANCEL 1 2 20')
        self.sim._read_line('ALERT 1 3 1000')
        self.sim._read_line('CANCEL 8 3 20')
        self.sim._read_line('ALERT 3 2 101')
        self.sim._read_line('CANCEL 6 2 230')
        self.sim.sort_messages()
        current = self.sim.get_current_messages()
        for message in current:
            self.assertEqual(20, message.time)
        self.assertEqual(4, len(current))

    def test_start_simulation(self):
        self.sim._read_line('LENGTH 2')
        self.sim.sort_messages()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.sim.start_simulation()
        self.assertEqual('@120000: END\n', output.getvalue())
    def test_sort_by_id(self):
        self.sim._read_line('CANCEL 2 3 20')
        self.sim._read_line('ALERT 1 2 20')
        self.sim._read_line('CANCEL 3 2 20')
        self.sim._read_line('CANCEL 3 2 20')
        self.sim._read_line('CANCEL 4 2 20')
        self.sim._read_line('CANCEL 2 2 20')
        self.sim._read_line('CANCEL 6 2 20')
        self.sim.messages.append(Message('END', None, None, self.sim.length, None, None))
        current = self.sim.get_current_messages()
        current_id = self.sim.sort_by_id(current)
        self.assertEqual(2, current_id[0].sender)
        self.assertEqual(1, current_id[1].sender)
        self.assertEqual(3, current_id[2].sender)
        self.assertEqual(3, current_id[3].sender)
        self.assertEqual(4, current_id[4].sender)
        self.assertEqual(2, current_id[5].sender)
        self.assertEqual(6, current_id[6].sender)
    def test_get_single_id(self):
        self.sim._read_line('CANCEL 2 3 30')
        self.sim._read_line('ALERT 1 2 20')
        self.sim._read_line('CANCEL 1 2 20')
        self.sim.messages.append(Message('END', None, None, self.sim.length, None, None))
        current = self.sim.get_current_messages()
        current_id = self.sim.sort_by_id(current)
        current_device = self.sim.get_single_id(current_id)
        for message in current_device:
            self.assertEqual(2, message.sender)
    def test_get_single_id_to_zero(self):
        self.sim._read_line('ALERT 1 2 20')
        self.sim._read_line('CANCEL 1 3 20')
        self.sim.messages.append(Message('END', None, None, self.sim.length, None, None))
        current = self.sim.get_current_messages()
        current_id = self.sim.sort_by_id(current)
        current_device = self.sim.get_single_id(current_id)
        for message in current_device:
            self.assertEqual(1, message.sender)

    def test_send(self):
        self.sim._read_line('ALERT 1 Boo 20')
        self.sim._read_line('DEVICE 1')
        self.sim._read_line('DEVICE 2')
        self.sim._read_line('PROPAGATE 1 2 100')
        self.sim.sort_messages()
        self.sim.set_device_rules()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.sim.devices['1'].send(self.sim.messages[0])
        self.assertEqual('@20: #1 SENT ALERT TO #2: Boo\n', output.getvalue())

    def test_send_cancellation(self):
        self.sim._read_line('CANCEL 1 Boo 20')
        self.sim._read_line('DEVICE 1')
        self.sim._read_line('DEVICE 2')
        self.sim._read_line('PROPAGATE 1 2 100')
        self.sim.sort_messages()
        self.sim.set_device_rules()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.sim.devices['1'].send(self.sim.messages[0])
        self.assertEqual('@20: #1 SENT CANCELLATION TO #2: Boo\n', output.getvalue())

    def test_receive(self):
        self.sim._read_line('CANCEL 1 Boo 20')
        self.sim._read_line('DEVICE 1')
        self.sim._read_line('DEVICE 2')
        self.sim._read_line('PROPAGATE 1 2 100')
        self.sim.sort_messages()
        self.sim.set_device_rules()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.sim.devices['1'].send(self.sim.messages[0])
        self.assertEqual('@20: #1 SENT CANCELLATION TO #2: Boo\n', output.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.sim.devices['2'].receive(self.sim.messages[0])
        self.assertEqual('@120: #2 RECEIVED CANCELLATION FROM #1: Boo\n', output.getvalue())

    def test_receive_alert(self):
        self.sim._read_line('ALERT 1 Boo 20')
        self.sim._read_line('DEVICE 1')
        self.sim._read_line('DEVICE 2')
        self.sim._read_line('PROPAGATE 1 2 100')
        self.sim.sort_messages()
        self.sim.set_device_rules()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.sim.devices['1'].send(self.sim.messages[0])
        self.assertEqual('@20: #1 SENT ALERT TO #2: Boo\n', output.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.sim.devices['2'].receive(self.sim.messages[0])
        self.assertEqual('@120: #2 RECEIVED ALERT FROM #1: Boo\n', output.getvalue())

    def test_receive_alert_after_cancellation(self):
        self.sim._read_line('ALERT 1 Boo 20')
        self.sim._read_line('DEVICE 1')
        self.sim._read_line('DEVICE 2')
        self.sim._read_line('PROPAGATE 1 2 100')
        self.sim.sort_messages()
        self.sim.set_device_rules()
        self.sim.devices['2'].cancellations.add('Boo')
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.sim.devices['1'].send(self.sim.messages[0])
        self.assertEqual('@20: #1 SENT ALERT TO #2: Boo\n', output.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.sim.devices['2'].receive(self.sim.messages[0])
        self.assertEqual('@120: #2 RECEIVED ALERT FROM #1: Boo\n', output.getvalue())

    def test_receive_cancel_after_cancellation(self):
        self.sim._read_line('CANCEL 1 Boo 20')
        self.sim._read_line('DEVICE 1')
        self.sim._read_line('DEVICE 2')
        self.sim._read_line('PROPAGATE 1 2 100')
        self.sim.sort_messages()
        self.sim.set_device_rules()
        self.sim.devices['2'].cancellations.add('Boo')
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.sim.devices['1'].send(self.sim.messages[0])
        self.assertEqual('@20: #1 SENT CANCELLATION TO #2: Boo\n', output.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.sim.devices['2'].receive(self.sim.messages[0])
        self.assertEqual('@120: #2 RECEIVED CANCELLATION FROM #1: Boo\n', output.getvalue())

    def make_test_file() -> Path:
        with tempfile.NamedTemporaryFile(mode = 'w', encoding = 'utf-8',
                                         delete = False) as input_file:
            input_file.write('LENGTH 1\n')
            input_file.write('DEVICE 1\n')
            input_file.write('DEVICE 2\n')
            input_file.write('DEVICE 3\n')
            input_file.write('DEVICE 4\n')
            input_file.write('PROPAGATE 1 2 120\n')
            input_file.write('PROPAGATE 2 3 200\n')
            input_file.write('PROPAGATE 3 4 320\n')
            input_file.write('PROPAGATE 4 1 900\n')
            input_file.write('ALERT 1 BAD 0\n')
            input_file.write('CANCEL 3 BAD 200\n')
            input_file.write('ALERT 1 BAD 9000\n')
            input_file.write('CANCEL 2 BAD 9000\n')
        return Path(input_file.name)

    file_path = str(make_test_file())
    @patch('builtins.input', return_value = file_path)
    def test_file_path(self, mock_input):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            project1.main()
        self.assertEqual("@0: #1 SENT ALERT TO #2: BAD\n"
                         "@120: #2 RECEIVED ALERT FROM #1: BAD\n"
                         "@120: #2 SENT ALERT TO #3: BAD\n"
                         "@200: #3 SENT CANCELLATION TO #4: BAD\n"
                         "@320: #3 RECEIVED ALERT FROM #2: BAD\n"
                         "@520: #4 RECEIVED CANCELLATION FROM #3: BAD\n"
                         "@520: #4 SENT CANCELLATION TO #1: BAD\n"
                         "@1420: #1 RECEIVED CANCELLATION FROM #4: BAD\n"
                         "@1420: #1 SENT CANCELLATION TO #2: BAD\n"
                         "@1540: #2 RECEIVED CANCELLATION FROM #1: BAD\n"
                         "@1540: #2 SENT CANCELLATION TO #3: BAD\n"
                         "@1740: #3 RECEIVED CANCELLATION FROM #2: BAD\n"
                         "@60000: END\n"
                         , output.getvalue())


if __name__ == '__main__':
    unittest.main()
