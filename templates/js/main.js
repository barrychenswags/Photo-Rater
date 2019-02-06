function submitVote(name)
{
    var photoID = name + "photos";
    var voteID = name + "vote";

    document.getElementById(photoID).style.display = 'none';
    document.getElementById(voteID).style.display = 'block';

    //need code for incrementing vote
}

function undoUploadImg(name)
{
    document.getElementById(name).style.display = 'none';
}

function displayVoteStartedMsg()
{
    document.getElementById("msgVoteStarted").style.display = 'block';
}