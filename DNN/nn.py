class Solution:
    def maxPathSum(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        m = float("-inf")
        def sub(root):
            global m
            if not root:
                return 0
            else:
                mm = max(root.val,root.val + sub(root.left),root.val + sub(root.right),root.val + sub(root.left) + sub(root.right))
                if mm > m:
                    m = mm
                return mm
        sub(root)
        return m