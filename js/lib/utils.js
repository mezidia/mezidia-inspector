const leaveComment = async (context, comment) => {
  return await context.createComment(comment);
}

module.exports={leaveComment}
