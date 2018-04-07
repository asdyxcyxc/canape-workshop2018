# This pulls in the canape library namespaces
import CANAPE.Nodes
import CANAPE.DataFrames
import CANAPE.Net.Layers;

def XorFrame(frame, xorValue):
    data = frame.ToArray()
    for i in range(len(data)):
        data[i] = data[i] ^ xorValue
           
    return CANAPE.DataFrames.DataFrame(data)

# Simple example script to implement a layer which xor's bytes with a known value
class XorNetworkLayer(CANAPE.Net.Layers.DynamicNetworkLayer):

    def GetXor(self):
        xorkey = self.Meta.GetMeta('XORKey')
        self.Logger.LogInfo("XORKEY: {0}", xorkey)
        return xorkey

    # This function is a generator, yield each frame you want
    def ReadClientFrames(self, client):
        self.Logger.LogInfo("Starting to read client frames")
        frame = client.Read()
        while frame is not None:
            yield XorFrame(frame, self.GetXor())
            frame = client.Read()
        
    # This function is a generator, yield each frame you want
    def ReadServerFrames(self, server):
        self.Logger.LogInfo("Starting to read server frames")
        frame = server.Read()
        while frame is not None:
            yield XorFrame(frame, self.GetXor())
            frame = server.Read()
        
    def WriteClientFrame(self, client, frame):
        client.Write(XorFrame(frame, self.GetXor()))
        
    def WriteServerFrame(self, server, frame):
        server.Write(XorFrame(frame, self.GetXor()))