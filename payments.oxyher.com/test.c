#include<stdio.h>
#include<stdlib.h>

struct queue_t 
{
    int data;
    struct queue_t * link;
};

void enqueue(struct queue_t **q , int data)
{
    struct queue_t * temp = (struct queue_t *) malloc(sizeof(struct queue_t));
    struct queue_t * prev = (struct queue_t *) malloc(sizeof(struct queue_t));
    prev = (*q);
    temp->data = data;
    temp->link = NULL;
    
    if(prev == NULL) {
        (*q) = temp;
        printf("ELEMENT ENQUEUED : %d \n",(*q)->data);
    } else {
        while((*q)->link != NULL) {
            (*q) = (*q)->link;
        }

        (*q)->link = temp;
        printf("ELEMENT ENQUEUED : %d \n",(temp)->data);
        (*q) = prev;
    }
}
void dequeue(struct queue_t **q) 
{
    struct queue_t * temp = (struct queue_t *) malloc(sizeof(struct queue_t));
    struct queue_t * prev = (struct queue_t *) malloc(sizeof(struct queue_t));
    prev = (*q);

    
    if(prev == NULL) {
        printf("NO ELEMENT FOUND...\n");
    } else {
       printf("ELEMENT DEQUEUED : %d\n",prev->data);
       temp = prev->link;
       free(*q);
       (*q) = temp;
    }
}

void display(struct queue_t *p)
{
    if(p == NULL) {
        printf("NO ELEMENTS FOUND....\n");
        return;
    }
    while(p != NULL) {
        printf("%d ",p->data);
        p = p->link;
        if(p != NULL) {
            printf(" -> ");
        }
    }
    printf("\n");
}
int main() {
    struct queue_t * top = NULL;
    // struct queue_t * end = NULL;
    int choice = 0;
    int data;
    do {
        printf("1. enqueue\n");
        printf("2. dequeue\n");
        printf("3. display\n");
        printf("4. exit\n");
        printf("Enter the choice : ");
        scanf("%d",&choice);
        if(choice == 1) {
            printf("Enter the data : ");
            scanf("%d", &data);
            enqueue(&top, data);
        }
        else if(choice == 2) {
            dequeue(&top);
        }
        else if(choice == 3) {
            display(top);
        }
        
    } while(choice != 4);
    
}