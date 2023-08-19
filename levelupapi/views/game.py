"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game
from levelupapi.models import Gamer
from levelupapi.models import GameType


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        
        # game = Game.objects.get(pk=pk)
        try:
            game_type = Game.objects.get(pk=pk)
            serializer = GameSerializer(game_type)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        
        games = Game.objects.all()
        
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type=game_type)
            
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
    	
        gamer = Gamer.objects.get(uid=request.data["userId"])
        game_type = GameType.objects.get(pk=request.data["gameType"])
        
        game = Game.objects.create(
			title=request.data["title"],
			maker=request.data["maker"],
			number_of_players=request.data["numberOfPlayers"],
			skill_level=request.data["skillLevel"],
			game_type=game_type,
			gamer=gamer,
		)
        serializer = GameSerializer(game)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]

        game_type = GameType.objects.get(pk=request.data["gameType"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = ('id', 'game_type', 'title', 'maker', 'gamer', 'number_of_players', 'skill_level')
        depth = 1
