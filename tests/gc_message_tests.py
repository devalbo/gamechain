import unittest
import gc_message


class MessageChainTests(unittest.TestCase):
    def test_multiple_stt_messages_invalid(self):

        # txid, sender_addr, receiver_addr, msg_type, msg
        msg1 = gc_message.GcMessage("", "", "", gc_message.MSG_STT, "")
        msg2 = gc_message.GcMessage("", "", "", gc_message.MSG_STT, "")

        messages = [msg1, msg2]
        with self.assertRaises(Exception):
            gc_message.build_gc_message_chain(messages)

    def test_zero_stt_messages_invalid(self):

        # txid, sender_addr, receiver_addr, msg_type, msg
        msg1 = gc_message.GcMessage("", "", "", gc_message.MSG_TMT, "")
        msg2 = gc_message.GcMessage("", "", "", gc_message.MSG_TMT, "")

        messages = [msg1, msg2]
        with self.assertRaises(Exception):
            gc_message.build_gc_message_chain(messages)