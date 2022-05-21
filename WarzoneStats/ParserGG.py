from statistics import mean

class Parser:
    
    def __init__(self):
        pass

    def get_average_lobby_kd(self, stats):
        """Parses the stats response from ApiGG module and returns the average lobby kd of all the matches in the response.

            Parameters
            ----------
            stats : dict
                The return value of ApiGG.get_stats(). An example of this response is in ./Sample\ Endpoint\ Response/apiGGResponse.json
            Raises
            ------
            ValueError
                If stats is either None or contains invalid json structure. ./Sample\ Endpoint\ Response/apiGGResponse.json
                contains proper structure 
        """
        if stats is None:
            raise ValueError('Stats incorrectly formatted or None, make sure you are passing in the resposne from ApiGG.get_stats()')
        try:
            kds = []
            for match in stats['matches']:
                matchKd = float(match['matchStatData']['playerAverage'])
                kds.append(matchKd)
            return mean(kds)
        except Exception as e:
            print(e)
            raise ValueError('Stats incorrectly formatted or None, make sure you are passing in the resposne from ApiGG.get_stats()')