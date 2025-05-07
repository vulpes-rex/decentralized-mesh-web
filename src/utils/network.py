class NetworkUtils:
    @staticmethod
    def calculate_packet_size(data, overhead=20):
        #\"\"\"Calculate required packet size including overhead\"\"\"
        return len(data) + overhead
        
    @staticmethod
    def estimate_transmission_time(data_size, bandwidth=1200):
        #\"\"\"Estimate transmission time in seconds\"\"\"
        return data_size / bandwidth
        
    @staticmethod
    def optimize_packet_size(data_size, mtu=250):
        #\"\"\"Optimize packet size based on MTU\"\"\"
        if data_size <= mtu:
            return data_size
        
        # Find optimal packet size
        packet_size = mtu
        while data_size % packet_size != 0 and packet_size > 1:
            packet_size -= 1
            
        return packet_size